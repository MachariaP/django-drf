from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Author, Book, Category


class AuthorAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )

    def test_get_authors_list(self):
        """Test retrieving list of authors."""
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_author_detail(self):
        """Test retrieving a single author."""
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john@example.com')

    def test_create_author(self):
        """Test creating a new author."""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com'
        }
        response = self.client.post('/api/authors/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_update_author(self):
        """Test updating an author."""
        data = {'first_name': 'Johnny'}
        response = self.client.patch(f'/api/authors/{self.author.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.first_name, 'Johnny')

    def test_delete_author(self):
        """Test deleting an author."""
        response = self.client.delete(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_author_without_authentication(self):
        """Test that unauthenticated users cannot create authors."""
        self.client.credentials()  # Remove authentication
        data = {
            'first_name': 'Test',
            'last_name': 'Author',
            'email': 'test@example.com'
        }
        response = self.client.post('/api/authors/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
        
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            author=self.author,
            publication_date='2023-01-01',
            pages=300,
            price=29.99
        )

    def test_get_books_list(self):
        """Test retrieving list of books."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_books_by_status(self):
        """Test filtering books by status."""
        response = self.client.get('/api/books/?status=available')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self):
        """Test searching books."""
        response = self.client.get('/api/books/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class HealthCheckAPITestCase(APITestCase):
    """Test cases for the health check endpoint."""
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
    
    def test_health_check_success(self):
        """Test health check endpoint returns 200 OK."""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
        self.assertEqual(response.data['database'], 'connected')
        self.assertEqual(response.data['api'], 'running')
    
    def test_health_check_no_authentication_required(self):
        """Test health check endpoint doesn't require authentication."""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRegistrationAPITestCase(APITestCase):
    """Test cases for user registration endpoint."""
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'first_name': 'New',
            'last_name': 'User'
        }
    
    def test_register_user_success(self):
        """Test successful user registration."""
        response = self.client.post('/api/register/', self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')
        
        # Verify user was created in database
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Verify token was created
        user = User.objects.get(username='newuser')
        self.assertTrue(Token.objects.filter(user=user).exists())
    
    def test_register_user_missing_fields(self):
        """Test registration fails with missing required fields."""
        # Missing password
        data = {'username': 'testuser', 'email': 'test@example.com'}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_register_user_duplicate_username(self):
        """Test registration fails with duplicate username."""
        # Create a user first
        User.objects.create_user(username='existinguser', password='pass123', email='existing@example.com')
        
        # Try to create another user with same username
        data = {
            'username': 'existinguser',
            'email': 'different@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username already exists', response.data['error'])
    
    def test_register_user_duplicate_email(self):
        """Test registration fails with duplicate email."""
        # Create a user first
        User.objects.create_user(username='user1', password='pass123', email='same@example.com')
        
        # Try to create another user with same email
        data = {
            'username': 'user2',
            'email': 'same@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email already exists', response.data['error'])
    
    def test_register_user_short_password(self):
        """Test registration fails with password less than 8 characters."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('at least 8 characters', response.data['error'])
    
    def test_register_user_can_login_with_token(self):
        """Test that registered user can authenticate with the returned token."""
        # Register a new user
        response = self.client.post('/api/register/', self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = response.data['token']
        
        # Use the token to access a protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
