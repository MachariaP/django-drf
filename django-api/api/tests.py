from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Author, Book, Category, Publisher, Review


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
    """Test cases for user registration endpoint - DEPRECATED: Use AuthenticationAPITestCase instead."""
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
    
    def test_register_user_success(self):
        """Test successful user registration."""
        response = self.client.post('/api/auth/register/', self.valid_user_data, format='json')
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
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password' in response.data or 'password_confirm' in response.data)
    
    def test_register_user_duplicate_username(self):
        """Test registration fails with duplicate username."""
        # Create a user first
        User.objects.create_user(username='existinguser', password='SecurePass123!', email='existing@example.com')
        
        # Try to create another user with same username
        data = {
            'username': 'existinguser',
            'email': 'different@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_register_user_duplicate_email(self):
        """Test registration fails with duplicate email."""
        # Create a user first
        User.objects.create_user(username='user1', password='SecurePass123!', email='same@example.com')
        
        # Try to create another user with same email
        data = {
            'username': 'user2',
            'email': 'same@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_register_user_short_password(self):
        """Test registration fails with password less than 8 characters."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short',
            'password_confirm': 'short'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_register_user_can_login_with_token(self):
        """Test that registered user can authenticate with the returned token."""
        # Register a new user
        response = self.client.post('/api/auth/register/', self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = response.data['token']
        
        # Use the token to access a protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticationAPITestCase(APITestCase):
    """Comprehensive test cases for authentication endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.logout_url = '/api/auth/logout/'
        self.password_change_url = '/api/auth/change-password/'
        self.profile_url = '/api/auth/profile/'
        
        # Valid user data for testing
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_registration_success(self):
        """Test successful user registration with valid data."""
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['email'], 'test@example.com')
        self.assertEqual(response.data['message'], 'User registered successfully')
    
    def test_user_registration_duplicate_username(self):
        """Test registration fails with duplicate username."""
        # Create first user
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Try to create another user with same username
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        response = self.client.post(self.register_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_user_registration_duplicate_email(self):
        """Test registration fails with duplicate email."""
        # Create first user
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Try to create another user with same email
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['username'] = 'different'
        response = self.client.post(self.register_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_user_registration_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        data = self.valid_user_data.copy()
        data['password_confirm'] = 'DifferentPass123!'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_confirm', response.data)
    
    def test_user_registration_weak_password(self):
        """Test registration fails with weak password using Django validators."""
        data = self.valid_user_data.copy()
        data['password'] = '12345'
        data['password_confirm'] = '12345'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_user_registration_common_password(self):
        """Test registration fails with common password."""
        data = self.valid_user_data.copy()
        data['password'] = 'password123'
        data['password_confirm'] = 'password123'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_user_login_success(self):
        """Test successful login with valid credentials."""
        # Register user first
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Login
        login_data = {
            'username': 'testuser',
            'password': 'SecurePass123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Login successful')
    
    def test_user_login_invalid_credentials(self):
        """Test login fails with invalid credentials."""
        # Register user first
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Try to login with wrong password
        login_data = {
            'username': 'testuser',
            'password': 'WrongPassword123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_user_login_nonexistent_user(self):
        """Test login fails with non-existent user."""
        login_data = {
            'username': 'nonexistent',
            'password': 'SomePassword123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_logout_success(self):
        """Test successful logout."""
        # Register and login
        register_response = self.client.post(self.register_url, self.valid_user_data, format='json')
        token = register_response.data['token']
        
        # Logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify token is invalidated
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_logout_without_auth(self):
        """Test logout fails without authentication."""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_profile_success(self):
        """Test getting user profile with valid token."""
        # Register user
        register_response = self.client.post(self.register_url, self.valid_user_data, format='json')
        token = register_response.data['token']
        
        # Get profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_get_user_profile_without_auth(self):
        """Test getting profile fails without authentication."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_password_change_success(self):
        """Test successful password change."""
        # Register user
        register_response = self.client.post(self.register_url, self.valid_user_data, format='json')
        token = register_response.data['token']
        
        # Change password
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        change_data = {
            'old_password': 'SecurePass123!',
            'new_password': 'NewSecurePass456!',
            'new_password_confirm': 'NewSecurePass456!'
        }
        response = self.client.post(self.password_change_url, change_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('token', response.data)  # New token issued
        
        # Verify old token is invalidated
        old_token = token
        new_token = response.data['token']
        self.assertNotEqual(old_token, new_token)
        
        # Verify can login with new password
        self.client.credentials()
        login_data = {
            'username': 'testuser',
            'password': 'NewSecurePass456!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_password_change_wrong_old_password(self):
        """Test password change fails with wrong old password."""
        # Register user
        register_response = self.client.post(self.register_url, self.valid_user_data, format='json')
        token = register_response.data['token']
        
        # Try to change password with wrong old password
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        change_data = {
            'old_password': 'WrongOldPass123!',
            'new_password': 'NewSecurePass456!',
            'new_password_confirm': 'NewSecurePass456!'
        }
        response = self.client.post(self.password_change_url, change_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)
    
    def test_password_change_new_passwords_mismatch(self):
        """Test password change fails when new passwords don't match."""
        # Register user
        register_response = self.client.post(self.register_url, self.valid_user_data, format='json')
        token = register_response.data['token']
        
        # Try to change password with mismatched new passwords
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        change_data = {
            'old_password': 'SecurePass123!',
            'new_password': 'NewSecurePass456!',
            'new_password_confirm': 'DifferentPass456!'
        }
        response = self.client.post(self.password_change_url, change_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password_confirm', response.data)
    
    def test_password_change_weak_new_password(self):
        """Test password change fails with weak new password."""
        # Register user
        register_response = self.client.post(self.register_url, self.valid_user_data, format='json')
        token = register_response.data['token']
        
        # Try to change to weak password
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        change_data = {
            'old_password': 'SecurePass123!',
            'new_password': '12345',
            'new_password_confirm': '12345'
        }
        response = self.client.post(self.password_change_url, change_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
    
    def test_password_change_without_auth(self):
        """Test password change fails without authentication."""
        change_data = {
            'old_password': 'SecurePass123!',
            'new_password': 'NewSecurePass456!',
            'new_password_confirm': 'NewSecurePass456!'
        }
        response = self.client.post(self.password_change_url, change_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed."""
        # Register user
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Get user from database
        user = User.objects.get(username='testuser')
        
        # Verify password is hashed (not stored in plaintext)
        self.assertNotEqual(user.password, 'SecurePass123!')
        self.assertTrue(user.password.startswith('pbkdf2_sha256'))
        
        # Verify password can be checked
        self.assertTrue(user.check_password('SecurePass123!'))


class ReviewPermissionTestCase(APITestCase):
    """Test cases for review permission enforcement."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create two users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123',
            email='user2@example.com'
        )
        
        # Create tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        # Create test data
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author',
            email='author@example.com'
        )
        
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            author=self.author,
            publication_date='2023-01-01',
            pages=300,
            price=29.99
        )
        
        # Create a review by user1
        self.review = Review.objects.create(
            book=self.book,
            user=self.user1,
            rating=5,
            title='Great Book',
            comment='This is an excellent book!'
        )
    
    def test_unauthenticated_can_read_reviews(self):
        """Test that unauthenticated users can read reviews."""
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_authenticated_user_can_create_review(self):
        """Test that authenticated users can create reviews."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        data = {
            'book': self.book.id,
            'rating': 4,
            'title': 'Good Book',
            'comment': 'I enjoyed this book.'
        }
        # Note: user1 already has a review for this book, so this will fail due to unique_together
        # Let's create a new book for this test
        new_book = Book.objects.create(
            title='Another Book',
            isbn='9876543210987',
            author=self.author,
            publication_date='2023-01-01',
            pages=200,
            price=19.99
        )
        data['book'] = new_book.id
        response = self.client.post('/api/reviews/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_unauthenticated_cannot_create_review(self):
        """Test that unauthenticated users cannot create reviews."""
        data = {
            'book': self.book.id,
            'rating': 4,
            'title': 'Good Book',
            'comment': 'I enjoyed this book.'
        }
        response = self.client.post('/api/reviews/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_owner_can_update_own_review(self):
        """Test that review owner can update their own review."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        data = {
            'rating': 4,
            'title': 'Updated Title',
            'comment': 'Updated comment.'
        }
        response = self.client.patch(f'/api/reviews/{self.review.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
    
    def test_owner_can_delete_own_review(self):
        """Test that review owner can delete their own review."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.delete(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
    
    def test_non_owner_cannot_update_review(self):
        """Test that non-owner cannot update another user's review."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        data = {
            'rating': 1,
            'title': 'Malicious Update',
            'comment': 'Trying to modify someone elses review.'
        }
        response = self.client.patch(f'/api/reviews/{self.review.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify review was not modified
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Great Book')
        self.assertEqual(self.review.rating, 5)
    
    def test_non_owner_cannot_delete_review(self):
        """Test that non-owner cannot delete another user's review."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.delete(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify review still exists
        self.assertEqual(Review.objects.count(), 1)
    
    def test_unauthenticated_cannot_update_review(self):
        """Test that unauthenticated users cannot update reviews."""
        data = {
            'rating': 1,
            'title': 'Unauthorized Update'
        }
        response = self.client.patch(f'/api/reviews/{self.review.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthenticated_cannot_delete_review(self):
        """Test that unauthenticated users cannot delete reviews."""
        response = self.client.delete(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
