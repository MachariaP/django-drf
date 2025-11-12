from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from api.pagination import StandardResultsSetPagination
from .models import Author, Category, Publisher, Book, Review
from .serializers import (
    AuthorSerializer, CategorySerializer, PublisherSerializer,
    BookListSerializer, BookDetailSerializer, ReviewSerializer
)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing authors.

    Provides full CRUD operations:
    - `list`: Retrieve all authors
    - `create`: Add a new author
    - `retrieve`: Get a single author
    - `update` / `partial_update`: Modify author details
    - `destroy`: Delete an author

    Features:
    - Search by `first_name`, `last_name`, `email`
    - Filter and order by `last_name`, `created_at`
    - Custom action: `/authors/{id}/books/` → list author's books
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['last_name', 'created_at']
    ordering = ['last_name']

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """
        Custom action: GET /api/authors/{id}/books/

        Returns a list of all books written by the specified author.
        Uses `BookListSerializer` for lightweight response.
        """
        author = self.get_object()
        books = author.books.all()
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing book categories.

    Supports full CRUD with:
    - Search in `name` and `description`
    - Ordering by `name` or `created_at`
    - Custom action: `/categories/{id}/books/` → books in category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """
        Custom action: GET /api/categories/{id}/books/

        Returns all books belonging to this category.
        Uses `BookListSerializer` for efficient serialization.
        """
        category = self.get_object()
        books = category.books.all()
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class PublisherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing publishers.

    Full CRUD operations with:
    - Search across `name`, `city`, `country`
    - Default ordering by `name`
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books with advanced querying and custom actions.

    Key features:
    - Optimized queryset with `select_related` and `prefetch_related`
    - Dynamic serializer: `BookListSerializer` (list) vs `BookDetailSerializer` (detail)
    - Filtering by `status`, `author`, `categories`, `publisher`
    - Search in `title`, `subtitle`, `isbn`, `description`
    - Ordering by `title`, `price`, `publication_date`, `created_at`

    Custom actions:
    - `/books/{id}/reviews/` → get all reviews
    - `/books/available/` → filter available books
    - `/books/bestsellers/` → top 10 most-reviewed books
    """
    queryset = Book.objects.select_related('author', 'publisher').prefetch_related('categories', 'reviews')
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'categories', 'publisher']
    search_fields = ['title', 'subtitle', 'isbn', 'description']
    ordering_fields = ['title', 'price', 'publication_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Use lightweight serializer for list views, detailed one for retrieve/update.
        """
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """
        Custom action: GET /api/books/{id}/reviews/

        Returns all reviews for the specified book.
        """
        book = self.get_object()
        reviews = book.reviews.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Custom action: GET /api/books/available/

        Returns only books with status='available'.
        """
        books = self.queryset.filter(status='available')
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """
        Custom action: GET /api/books/bestsellers/

        Returns top 10 books ranked by number of reviews (proxy for popularity).
        """
        from django.db.models import Count
        books = self.queryset.annotate(
            review_count=Count('reviews')
        ).order_by('-review_count')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15), name='dispatch')
    def list(self, request, *args, **kwargs):
        """
        Override list method to add caching for 15 minutes.
        """
        return super().list(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing book reviews.

    Features:
    - Auto-assigns `user` from authenticated request
    - Optional filtering: `?my_reviews=true` → only current user's reviews
    - Filter by `book`, `user`, `rating`
    - Order by `rating` or `created_at`

    Permissions:
    - Read: anyone
    - Write: authenticated users only
    """
    queryset = Review.objects.select_related('book', 'user')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['book', 'user', 'rating']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """
        Automatically set the review author to the current authenticated user.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Allow users to filter their own reviews using query param:
        Example: GET /api/reviews/?my_reviews=true
        """
        queryset = super().get_queryset()
        if self.request.query_params.get('my_reviews'):
            queryset = queryset.filter(user=self.request.user)
        return queryset
