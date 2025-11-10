# 📘 Complete Django REST Framework API Guide

> A comprehensive step-by-step guide to building a complete REST API with Django REST Framework, including advanced features and best practices.

---

## 📑 Table of Contents

1. [Introduction](#1-introduction)
2. [Project Setup from Scratch](#2-project-setup-from-scratch)
3. [Creating Your First Django App](#3-creating-your-first-django-app)
4. [Building Models](#4-building-models)
5. [Creating Serializers](#5-creating-serializers)
6. [Building Views and ViewSets](#6-building-views-and-viewsets)
7. [URL Configuration and Routing](#7-url-configuration-and-routing)
8. [Authentication and Permissions](#8-authentication-and-permissions)
9. [Advanced Features](#9-advanced-features)
10. [Testing Your API](#10-testing-your-api)
11. [API Documentation](#11-api-documentation)
12. [Deployment](#12-deployment)
13. [Best Practices](#13-best-practices)
14. [Troubleshooting](#14-troubleshooting)

---

## 1. Introduction

### What is Django REST Framework?

Django REST Framework (DRF) is a powerful and flexible toolkit for building Web APIs in Django. It provides:

- **Serialization** - Convert complex data types (like Django models) to native Python datatypes that can be easily rendered into JSON, XML, or other content types
- **Authentication** - Multiple authentication schemes including OAuth, token-based, and session-based
- **Permissions** - Fine-grained access control for your API endpoints
- **Browsable API** - A web-based interface for interacting with your API
- **ViewSets and Routers** - Simplified URL routing and view logic

### Why Use DRF?

✅ **Rapid Development** - Build APIs quickly with less boilerplate code  
✅ **Highly Customizable** - Extend and customize every component  
✅ **Well Documented** - Comprehensive documentation and active community  
✅ **Battle Tested** - Used by companies like Mozilla, Red Hat, and Eventbrite  
✅ **Standards Compliant** - Follows REST architectural principles  

---

## 2. Project Setup from Scratch

### Step 1: Install Python and Verify Installation

```bash
# Check Python version (3.8+ recommended)
python --version

# Check pip version
pip --version
```

### Step 2: Create Project Directory

```bash
# Create and navigate to project directory
mkdir my-django-api
cd my-django-api
```

### Step 3: Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Django and DRF

```bash
# Install Django
pip install django

# Install Django REST Framework
pip install djangorestframework

# Install additional useful packages
pip install django-cors-headers  # For CORS support
pip install django-filter         # For advanced filtering
pip install drf-spectacular       # For API documentation
pip install python-dotenv         # For environment variables
pip install psycopg2-binary       # For PostgreSQL (optional)
pip install pillow                # For image handling (optional)
```

### Step 5: Create Django Project

```bash
# Create Django project
django-admin startproject config .

# Note: The dot (.) creates the project in the current directory
```

### Step 6: Configure Settings

Edit `config/settings.py`:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
]

# Add CORS middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# CORS settings (for development)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
]

# For development, you can allow all origins (NOT for production!)
# CORS_ALLOW_ALL_ORIGINS = True
```

### Step 7: Create Requirements File

```bash
# Save installed packages to requirements.txt
pip freeze > requirements.txt
```

### Step 8: Initial Migration

```bash
# Create initial database tables
python manage.py migrate
```

### Step 9: Create Superuser

```bash
# Create admin user
python manage.py createsuperuser
```

### Step 10: Run Development Server

```bash
# Start the server
python manage.py runserver

# Visit http://127.0.0.1:8000/ to see Django welcome page
# Visit http://127.0.0.1:8000/admin/ to access admin panel
```

---

## 3. Creating Your First Django App

### Step 1: Create an App

```bash
# Create a new app called 'api' or 'books' (example)
python manage.py startapp books
```

### Step 2: Register the App

Add to `config/settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'books',  # Add your app
]
```

### App Structure

After creating an app, you'll have:

```
books/
├── __init__.py
├── admin.py          # Admin interface configuration
├── apps.py           # App configuration
├── models.py         # Database models
├── tests.py          # Tests
├── views.py          # Views/ViewSets
└── migrations/       # Database migrations
```

---

## 4. Building Models

### Step 1: Define Your Models

Edit `books/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'Authors'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    """Model representing a book category."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Model representing a publisher."""
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book."""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('coming_soon', 'Coming Soon'),
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='books',
        blank=True
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    publication_date = models.DateField()
    pages = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(blank=True)
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
        ]

    def __str__(self):
        return self.title


class Review(models.Model):
    """Model representing a book review."""
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'user']  # One review per user per book

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"
```

### Step 2: Register Models in Admin

Edit `books/admin.py`:

```python
from django.contrib import admin
from .models import Author, Category, Publisher, Book, Review


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country']
    search_fields = ['name', 'city', 'country']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'status', 'price', 'publication_date']
    list_filter = ['status', 'publication_date', 'categories']
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']
    filter_horizontal = ['categories']
    date_hierarchy = 'publication_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'title']
```

### Step 3: Create and Run Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

---

## 5. Creating Serializers

Serializers convert complex data types (like Django models) to Python datatypes that can be rendered into JSON.

### Step 1: Create Serializers File

Create `books/serializers.py`:

```python
from rest_framework import serializers
from .models import Author, Category, Publisher, Book, Review
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model."""
    full_name = serializers.ReadOnlyField()
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'birth_date', 'biography', 'email', 'website',
            'books_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_books_count(self, obj):
        return obj.books.count()

    def validate_email(self, value):
        """Custom validation for email field."""
        if Author.objects.filter(email=value).exists():
            if not self.instance or self.instance.email != value:
                raise serializers.ValidationError(
                    "An author with this email already exists."
                )
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'books_count', 'created_at']
        read_only_fields = ['created_at']

    def get_books_count(self, obj):
        return obj.books.count()


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for Publisher model."""
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Publisher
        fields = [
            'id', 'name', 'address', 'city', 'country',
            'website', 'books_count', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_books_count(self, obj):
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for book lists."""
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    categories = serializers.StringRelatedField(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author_name', 'categories',
            'price', 'status', 'average_rating', 'publication_date'
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None


class BookDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual books."""
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        source='categories',
        write_only=True
    )
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(),
        source='publisher',
        write_only=True,
        required=False,
        allow_null=True
    )
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'subtitle', 'isbn', 'author', 'author_id',
            'categories', 'category_ids', 'publisher', 'publisher_id',
            'publication_date', 'pages', 'price', 'description',
            'cover_image', 'status', 'reviews_count', 'average_rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return None


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user = serializers.StringRelatedField(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'book', 'book_title', 'user', 'rating',
            'title', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_rating(self, value):
        """Ensure rating is between 1 and 5."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        """Override create to set the user from the request."""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'reviews_count']
        read_only_fields = ['id']

    def get_reviews_count(self, obj):
        return obj.reviews.count()
```

### Understanding Serializers

**Key Concepts:**

1. **ModelSerializer** - Automatically generates fields based on the model
2. **SerializerMethodField** - Custom fields calculated at serialization time
3. **read_only=True** - Field is shown but can't be modified via API
4. **write_only=True** - Field can be sent but won't appear in responses
5. **PrimaryKeyRelatedField** - Handle foreign key relationships
6. **Validation** - Custom validation methods for data integrity

---

## 6. Building Views and ViewSets

### Step 1: Create Views

Create `books/views.py`:

```python
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Category, Publisher, Book, Review
from .serializers import (
    AuthorSerializer, CategorySerializer, PublisherSerializer,
    BookListSerializer, BookDetailSerializer, ReviewSerializer
)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing authors.
    
    Provides `list`, `create`, `retrieve`, `update`, `partial_update`, 
    and `destroy` actions.
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
        """Get all books by a specific author."""
        author = self.get_object()
        books = author.books.all()
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Get all books in a specific category."""
        category = self.get_object()
        books = category.books.all()
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class PublisherViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing publishers."""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing books."""
    queryset = Book.objects.select_related('author', 'publisher').prefetch_related('categories', 'reviews')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'categories', 'publisher']
    search_fields = ['title', 'subtitle', 'isbn', 'description']
    ordering_fields = ['title', 'price', 'publication_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific book."""
        book = self.get_object()
        reviews = book.reviews.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available books."""
        books = self.queryset.filter(status='available')
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """Get bestselling books (most reviewed)."""
        from django.db.models import Count
        books = self.queryset.annotate(
            review_count=Count('reviews')
        ).order_by('-review_count')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing reviews."""
    queryset = Review.objects.select_related('book', 'user')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['book', 'user', 'rating']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Set the user when creating a review."""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Optionally restrict reviews to those by the requesting user."""
        queryset = super().get_queryset()
        if self.request.query_params.get('my_reviews'):
            queryset = queryset.filter(user=self.request.user)
        return queryset
```

### Understanding ViewSets

**Key Features:**

1. **ModelViewSet** - Provides all CRUD operations automatically
2. **@action decorator** - Create custom endpoints
3. **get_serializer_class()** - Use different serializers for different actions
4. **perform_create()** - Hook into object creation
5. **get_queryset()** - Dynamically filter querysets
6. **select_related/prefetch_related** - Optimize database queries

---

## 7. URL Configuration and Routing

### Step 1: Create App URLs

Create `books/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, CategoryViewSet, PublisherViewSet,
    BookViewSet, ReviewViewSet
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'publishers', PublisherViewSet, basename='publisher')
router.register(r'books', BookViewSet, basename='book')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
```

### Step 2: Include App URLs in Project URLs

Edit `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('books.urls')),
    
    # Authentication
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Available Endpoints

After setup, you'll have these endpoints:

```
GET    /api/authors/              - List all authors
POST   /api/authors/              - Create a new author
GET    /api/authors/{id}/         - Get author details
PUT    /api/authors/{id}/         - Update author
PATCH  /api/authors/{id}/         - Partial update author
DELETE /api/authors/{id}/         - Delete author
GET    /api/authors/{id}/books/   - Get author's books

GET    /api/categories/           - List all categories
POST   /api/categories/           - Create a new category
GET    /api/categories/{id}/      - Get category details
GET    /api/categories/{id}/books/ - Get category's books

GET    /api/books/                - List all books
POST   /api/books/                - Create a new book
GET    /api/books/{id}/           - Get book details
GET    /api/books/{id}/reviews/   - Get book's reviews
GET    /api/books/available/      - Get available books
GET    /api/books/bestsellers/    - Get bestsellers

GET    /api/reviews/              - List all reviews
POST   /api/reviews/              - Create a new review
GET    /api/reviews/{id}/         - Get review details

POST   /api/token/                - Get authentication token
```

---

## 8. Authentication and Permissions

### Token Authentication

#### Step 1: Generate Tokens for Users

```python
# In Django shell
python manage.py shell

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create token for a user
user = User.objects.get(username='admin')
token = Token.objects.create(user=user)
print(token.key)
```

#### Step 2: Use Token in API Requests

```bash
# Using curl
curl -X GET http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# Using httpie
http GET http://127.0.0.1:8000/api/books/ \
  "Authorization: Token YOUR_TOKEN_HERE"
```

### Custom Permissions

Create `books/permissions.py`:

```python
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        return obj.author == request.user


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow review owners to edit their reviews.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff
```

#### Use Custom Permissions in Views

```python
from .permissions import IsReviewOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]
```

---

## 9. Advanced Features

### 9.1 Filtering and Search

Already configured in ViewSets! Usage examples:

```bash
# Filter books by status
GET /api/books/?status=available

# Filter books by author
GET /api/books/?author=1

# Search books by title
GET /api/books/?search=Django

# Order books by price
GET /api/books/?ordering=price

# Combine filters
GET /api/books/?status=available&ordering=-price
```

### 9.2 Pagination

The default pagination is configured in settings. You can customize it:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Usage:

```bash
# Get first page
GET /api/books/

# Get second page
GET /api/books/?page=2
```

### 9.3 Custom Pagination

Create `books/pagination.py`:

```python
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000
```

Use in ViewSet:

```python
class BookViewSet(viewsets.ModelViewSet):
    # ...
    pagination_class = StandardResultsSetPagination
```

### 9.4 Throttling (Rate Limiting)

Configure in `settings.py`:

```python
REST_FRAMEWORK = {
    # ...
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

Custom throttle:

```python
# books/throttles.py
from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

### 9.5 Caching

Install Redis and configure caching:

```bash
pip install django-redis
```

Configure in `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

Use caching in views:

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class BookViewSet(viewsets.ModelViewSet):
    # ...
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

### 9.6 File Uploads

Configure media settings in `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Handle file uploads:

```python
# Serializer automatically handles file uploads
# Just make sure to use multipart/form-data in requests

# Example with curl:
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "title=Book Title" \
  -F "author_id=1" \
  -F "cover_image=@/path/to/image.jpg"
```

### 9.7 Versioning

Configure API versioning:

```python
# settings.py
REST_FRAMEWORK = {
    # ...
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

Update URLs:

```python
# config/urls.py
urlpatterns = [
    path('api/v1/', include('books.urls')),
    path('api/v2/', include('books.v2.urls')),  # For future version
]
```

---

## 10. Testing Your API

### Step 1: Create Tests

Create `books/tests.py`:

```python
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
```

### Step 2: Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test books.tests

# Run specific test class
python manage.py test books.tests.AuthorAPITestCase

# Run with verbosity
python manage.py test --verbosity=2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

---

## 11. API Documentation

### Using drf-spectacular for OpenAPI Documentation

Already configured! Access documentation at:

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

### Customize Documentation

Add docstrings and schema information:

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing books.
    
    list:
    Return a list of all books in the system.
    
    create:
    Create a new book instance.
    
    retrieve:
    Return the details of a specific book.
    
    update:
    Update all fields of a book.
    
    partial_update:
    Update specific fields of a book.
    
    destroy:
    Delete a book from the system.
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='status', description='Filter by status', required=False, type=str),
            OpenApiParameter(name='search', description='Search in title and description', required=False, type=str),
        ],
        responses={200: BookListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List all books with optional filtering."""
        return super().list(request, *args, **kwargs)
```

---

## 12. Deployment

### 12.1 Preparing for Production

#### Update Settings for Production

Create `config/settings_production.py`:

```python
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
```

### 12.2 Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=django_api
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=django_password
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/code
      - static_volume:/code/staticfiles
      - media_volume:/code/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/code/staticfiles
      - media_volume:/code/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 12.3 Deploy to Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn config.wsgi" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Initialize git and commit
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

---

## 13. Best Practices

### 13.1 Code Organization

```
project/
├── config/                 # Project settings
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                   # Django apps
│   ├── books/
│   ├── users/
│   └── common/
├── static/                 # Static files
├── media/                  # User uploads
├── templates/              # Templates
├── tests/                  # Tests
├── manage.py
└── requirements/
    ├── base.txt
    ├── development.txt
    └── production.txt
```

### 13.2 Environment Variables

Use `.env` file for sensitive data:

```bash
# .env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

Load in settings:

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

### 13.3 Database Optimization

```python
# Use select_related for foreign keys
books = Book.objects.select_related('author', 'publisher')

# Use prefetch_related for many-to-many
books = Book.objects.prefetch_related('categories', 'reviews')

# Use only() to fetch specific fields
books = Book.objects.only('title', 'price')

# Use defer() to exclude fields
books = Book.objects.defer('description')

# Use exists() instead of count()
if Book.objects.filter(status='available').exists():
    pass

# Use iterator() for large querysets
for book in Book.objects.iterator(chunk_size=100):
    process_book(book)
```

### 13.4 Security Checklist

✅ Use HTTPS in production  
✅ Set DEBUG=False in production  
✅ Use strong SECRET_KEY  
✅ Configure ALLOWED_HOSTS properly  
✅ Use CSRF protection  
✅ Implement rate limiting  
✅ Validate all user inputs  
✅ Use parameterized queries (ORM)  
✅ Keep dependencies updated  
✅ Use environment variables for secrets  
✅ Implement proper authentication  
✅ Set secure cookie flags  

---

## 14. Troubleshooting

### Common Issues and Solutions

#### Issue: CORS Errors

```python
# Install django-cors-headers
pip install django-cors-headers

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'corsheaders',
]

# Add to MIDDLEWARE (near the top)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# Configure CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

#### Issue: Authentication Not Working

```python
# Ensure TokenAuthentication is in settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Generate token for user
from rest_framework.authtoken.models import Token
token = Token.objects.create(user=user)

# Include token in requests
# Header: Authorization: Token YOUR_TOKEN_HERE
```

#### Issue: Slow Queries

```python
# Enable query logging in development
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Use django-debug-toolbar
pip install django-debug-toolbar
```

#### Issue: Migration Conflicts

```bash
# Show migrations
python manage.py showmigrations

# Create a merge migration
python manage.py makemigrations --merge

# Reset migrations (development only!)
# Delete all migration files except __init__.py
# Delete database
python manage.py makemigrations
python manage.py migrate
```

---

## 🎉 Conclusion

Congratulations! You now have a comprehensive understanding of building REST APIs with Django REST Framework. This guide covered:

- ✅ Project setup from scratch
- ✅ Creating models, serializers, and views
- ✅ Authentication and permissions
- ✅ Advanced features (filtering, pagination, caching)
- ✅ Testing and documentation
- ✅ Deployment strategies
- ✅ Best practices and troubleshooting

### Next Steps

1. **Expand the API** - Add more models and relationships
2. **Implement Webhooks** - Notify external systems of events
3. **Add Real-time Features** - Use Django Channels for WebSockets
4. **Integrate Third-party Services** - Payment gateways, email services, etc.
5. **Mobile App Integration** - Connect iOS/Android apps to your API
6. **Microservices** - Break down into smaller services
7. **GraphQL** - Implement GraphQL alongside REST using Graphene-Django

### Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **DRF Documentation**: https://www.django-rest-framework.org/
- **Two Scoops of Django**: Book on Django best practices
- **Real Python**: Tutorials and courses
- **Django Community**: Join the discussion on forums and Discord

---

**Happy Coding! 🚀**

*If you found this guide helpful, please star the repository and share it with others!*
