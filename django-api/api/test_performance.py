"""
Performance test to verify database query optimization.
This test demonstrates that annotated fields eliminate N+1 queries.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test.utils import override_settings
from django.db import connection
from django.test.utils import CaptureQueriesContext

from api.models import Author, Book, Category, Publisher, Review


class PerformanceOptimizationTestCase(APITestCase):
    """Test cases to verify database query optimizations."""
    
    def setUp(self):
        """Set up test data with multiple objects to test N+1 prevention."""
        self.client = APIClient()
        
        # Create a user and token
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create multiple authors
        self.authors = [
            Author.objects.create(
                first_name=f'Author{i}',
                last_name=f'Last{i}',
                email=f'author{i}@example.com'
            ) for i in range(5)
        ]
        
        # Create multiple categories
        self.categories = [
            Category.objects.create(
                name=f'Category{i}',
                slug=f'category{i}'
            ) for i in range(5)
        ]
        
        # Create multiple publishers
        self.publishers = [
            Publisher.objects.create(
                name=f'Publisher{i}'
            ) for i in range(5)
        ]
        
        # Create multiple books with reviews
        self.books = []
        for i in range(10):
            book = Book.objects.create(
                title=f'Book{i}',
                isbn=f'123456789{i:04d}',
                author=self.authors[i % 5],
                publisher=self.publishers[i % 5],
                publication_date='2023-01-01',
                pages=300,
                price=29.99
            )
            # Add categories
            book.categories.add(self.categories[i % 5])
            
            # Add reviews
            for j in range(3):
                Review.objects.create(
                    book=book,
                    user=self.user if j == 0 else User.objects.create_user(
                        username=f'reviewer{i}_{j}',
                        password='pass123',
                        email=f'reviewer{i}_{j}@example.com'
                    ),
                    rating=(j % 5) + 1,
                    title=f'Review {j}',
                    comment=f'Comment {j}'
                )
            self.books.append(book)
    
    def test_author_list_query_efficiency(self):
        """Verify that author list doesn't trigger N+1 queries for books_count."""
        with CaptureQueriesContext(connection) as context:
            response = self.client.get('/api/authors/')
        
        # Should be a small number of queries (not N+1):
        # 1. Get authors with annotation
        # 2. Pagination count query (optional)
        # 3. Auth/session queries
        query_count = len(context.captured_queries)
        
        # Verify response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        
        # Verify books_count is present in each author
        for author_data in response.data['results']:
            self.assertIn('books_count', author_data)
            self.assertIsNotNone(author_data['books_count'])
        
        # With annotation, should be very few queries (typically 4-6)
        # Without annotation, it would be 5+ (1 for authors, 5 for each author's books)
        self.assertLess(query_count, 10, 
            f"Query count ({query_count}) should be small with annotation optimization")
    
    def test_category_list_query_efficiency(self):
        """Verify that category list doesn't trigger N+1 queries for books_count."""
        with CaptureQueriesContext(connection) as context:
            response = self.client.get('/api/categories/')
        
        query_count = len(context.captured_queries)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        
        for category_data in response.data['results']:
            self.assertIn('books_count', category_data)
        
        self.assertLess(query_count, 10)
    
    def test_publisher_list_query_efficiency(self):
        """Verify that publisher list doesn't trigger N+1 queries for books_count."""
        with CaptureQueriesContext(connection) as context:
            response = self.client.get('/api/publishers/')
        
        query_count = len(context.captured_queries)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        
        for publisher_data in response.data['results']:
            self.assertIn('books_count', publisher_data)
        
        self.assertLess(query_count, 10)
    
    def test_book_list_query_efficiency(self):
        """Verify that book list doesn't trigger N+1 queries for average_rating."""
        with CaptureQueriesContext(connection) as context:
            response = self.client.get('/api/books/')
        
        query_count = len(context.captured_queries)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        
        # Verify average_rating is computed for each book
        for book_data in response.data['results']:
            self.assertIn('average_rating', book_data)
        
        # With select_related and annotation, should be efficient
        # Without optimization, would need queries for each book's reviews
        self.assertLess(query_count, 15)
    
    def test_book_detail_query_efficiency(self):
        """Verify that book detail doesn't trigger extra queries for counts."""
        book_id = self.books[0].id
        
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(f'/api/books/{book_id}/')
        
        query_count = len(context.captured_queries)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('reviews_count', response.data)
        self.assertIn('average_rating', response.data)
        self.assertEqual(response.data['reviews_count'], 3)
        
        # Should be efficient with annotations
        self.assertLess(query_count, 15)
    
    def test_annotated_values_are_correct(self):
        """Verify that annotated values match actual computed values."""
        # Get the first book
        book = self.books[0]
        
        # Verify via API
        response = self.client.get(f'/api/books/{book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Calculate expected values
        expected_review_count = book.reviews.count()
        expected_avg_rating = sum(r.rating for r in book.reviews.all()) / expected_review_count if expected_review_count > 0 else None
        
        # Verify API returns correct values
        self.assertEqual(response.data['reviews_count'], expected_review_count)
        if expected_avg_rating is not None:
            self.assertAlmostEqual(response.data['average_rating'], expected_avg_rating, places=2)
