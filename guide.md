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

Building a complete API begins with a proper development environment and installing necessary toolkits.

### Key Steps: Installation and Configuration

| Step | Command/Action | Purpose and Advantage (Why we do this) |
| :--- | :--- | :--- |
| **1. Environment** | `python -m venv venv` and `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows) | **Advantage:** Isolates project dependencies from the system Python installation, preventing version conflicts. This ensures your project's packages won't interfere with other Python projects or system tools. |
| **2. Dependencies** | `pip install django djangorestframework` | Installs the core tools. DRF is a flexible toolkit for building Web APIs in Django. Django provides the robust web framework foundation, while DRF extends it with powerful API-building capabilities. |
| **3. Core Third-Party** | `pip install django-cors-headers django-filter drf-spectacular` | **DRF relies on extensions** for crucial functions: `django-cors-headers` for handling Cross-Origin Resource Sharing (allows frontend apps on different domains to access your API); `django-filter` for advanced filtering capabilities (search, filter by fields); and `drf-spectacular` for generating API documentation (OpenAPI schema) automatically. |
| **4. Additional Tools** | `pip install python-dotenv psycopg2-binary pillow` | `python-dotenv` manages environment variables securely; `psycopg2-binary` enables PostgreSQL database connections for production; `pillow` handles image uploads and processing. |

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
    'corsheaders.middleware.CorsMiddleware',  # Add this BEFORE CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### REST Framework Global Settings

The global configuration in `settings.py` defines standard behaviors for the entire API, such as authentication and filtering.

```python
REST_FRAMEWORK = {
    # Authentication (Token and Session based)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # Permissions (Safe methods are allowed to all, write methods require authentication)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # Filtering/Search
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # Documentation
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

The provided structure focuses on a bookstore theme, defining relationships between key entities.

### Core Model Relationships

The schema defines several interconnected models with important database relationships:

*   **`Author`** and **`Book`**: A `ForeignKey` relationship means one Author can write many Books (`related_name='books'`). This is a **one-to-many** relationship.
    *   **Why this matters:** When you have an author object, you can access all their books using `author.books.all()` thanks to the `related_name`.
    
*   **`Category`** and **`Book`**: A `ManyToManyField` relationship means a Book can belong to many Categories, and a Category can contain many Books.
    *   **Real-world example:** A Django book might be in both "Web Development" and "Python Programming" categories.
    
*   **`Book`** and **`Review`**: A `ForeignKey` relationship where one Book can receive many Reviews.
    *   **Data integrity:** Using `on_delete=models.CASCADE` ensures that when a book is deleted, all its reviews are automatically deleted too.
    
*   **`User`** and **`Review`**: A `ForeignKey` relationship where one User can submit many Reviews.
    *   **Best Practice:** The `Review` model uses `unique_together = ['book', 'user']` to ensure that a single user can only leave one review per book, preventing duplicate reviews from the same user.

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

**Serialization** is the process of converting complex data types (like Django models or querysets) into native Python datatypes that can be easily rendered into standard content types like JSON or XML.

**Think of it like this:** Serializers are translators between your Django models (Python objects) and JSON (what the API sends/receives). They work both ways - turning database objects into JSON for responses, and validating/converting JSON into objects for saving to the database.

### Key Concepts and Best Practices

1.  **`ModelSerializer`**: This automatically generates fields based on the corresponding Django model, reducing boilerplate code and enabling rapid development.
    *   **Advantage:** Instead of manually defining every field, Django inspects your model and creates the appropriate serializer fields automatically.

2.  **`SerializerMethodField` (Custom Read Fields)**: Used when the data required in the API response is not a direct database field but must be calculated or aggregated at runtime.

    *   **Example 1 (`AuthorSerializer`)**: The `full_name` field is defined using `@property` on the model and automatically exposed as `full_name = serializers.ReadOnlyField()`. The `books_count` is calculated using `get_books_count(self, obj)` to count related books (`obj.books.count()`).
    *   **Example 2 (`BookDetailSerializer`)**: Calculates `average_rating` by iterating through related reviews.
    *   **Why this is useful:** These computed fields provide valuable information without storing redundant data in the database.

3.  **Handling Relationships (Read vs. Write)**: This is crucial for maintaining data integrity.

| Operation Type | DRF Field Used | Purpose and Advantage |
| :--- | :--- | :--- |
| **Read (Output)** | Nested Serializer (`author = AuthorSerializer(read_only=True)`) | **Advantage:** Provides rich, linked data structures (e.g., embedding the full author object within the book detail response). The client gets complete information without making multiple API calls. |
| **Write (Input)** | **`PrimaryKeyRelatedField`** (`author_id = serializers.PrimaryKeyRelatedField(...)`) | **Advantage:** Allows the client to send a simple ID (e.g., `author_id: 1`) in the request body, which DRF validates against the database queryset before saving. It uses `write_only=True` so the field is used for creation/update but does not appear in the response. This keeps the API clean and prevents confusion. |

4.  **Custom Validation**: Serializers allow fine-grained data validation before saving. For instance, the `AuthorSerializer` custom validates the uniqueness of the `email` field. The `ReviewSerializer` validates that the `rating` is between 1 and 5.
    *   **Security benefit:** Validation happens before data reaches the database, preventing invalid data and potential security issues.

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

1. **ModelSerializer** - Automatically generates fields based on the model, dramatically reducing code
2. **SerializerMethodField** - Custom fields calculated at serialization time (like `books_count`, `average_rating`)
3. **read_only=True** - Field is shown in responses but can't be modified via API (for computed or sensitive fields)
4. **write_only=True** - Field can be sent in requests but won't appear in responses (for IDs used in creation)
5. **PrimaryKeyRelatedField** - Handle foreign key relationships by accepting/returning IDs
6. **Validation** - Custom validation methods (`validate_<field_name>`) for data integrity

**Why this architecture?** By separating read and write serializers for relationships, we give clients rich, nested data when reading (GET requests) but accept simple IDs when writing (POST/PUT). This makes the API both informative and easy to use.

---

## 6. Building Views and ViewSets

**ViewSets** provide simplified URL routing and view logic by combining the logic for a set of related views (list, detail, create, update, destroy) into a single class.

**The Analogy:** Think of a **`ModelViewSet`** as a master chef who knows how to prepare all five standard meals (CRUD operations: Create, Read, Update, Delete, plus List). The **`DefaultRouter`** is the menu publisher; once the chef is hired (registered), the router automatically publishes the entire menu (all necessary endpoints) under clear, standardized paths, saving you the manual work of writing out every single dish on the menu card.

### The Power of `ModelViewSet`

The **`ModelViewSet`** class provides standard CRUD (Create, Retrieve, Update, Destroy) operations automatically, based on the defined `queryset` and `serializer_class`.

**What you get for free:**
- `list()` - GET /api/books/ - List all books
- `create()` - POST /api/books/ - Create a new book
- `retrieve()` - GET /api/books/{id}/ - Get a specific book
- `update()` - PUT /api/books/{id}/ - Update a book (all fields)
- `partial_update()` - PATCH /api/books/{id}/ - Update a book (some fields)
- `destroy()` - DELETE /api/books/{id}/ - Delete a book

### Database Optimization: `select_related` and `prefetch_related`

For performance, the `BookViewSet` utilizes database query optimization techniques:

```python
queryset = Book.objects.select_related('author', 'publisher').prefetch_related('categories', 'reviews')
```

| Method | Technical Definition | Simple English Explanation (Advantage) |
| :--- | :--- | :--- |
| **`select_related`** | Used for ForeignKey and OneToOne relationships. | **It fetches related objects in the same database query (a SQL JOIN).** This prevents the "N+1 query problem" for single related objects (like the Author or Publisher). Without this, loading 100 books would make 1 query for books + 100 queries for authors = 101 queries! With `select_related`, it's just 1 query. |
| **`prefetch_related`** | Used for ManyToMany and Reverse ForeignKey relationships. | **It performs a separate lookup for related objects, then joins them in Python.** This efficiently gathers multiple related objects (like Categories or Reviews) without excessive database trips. Instead of N queries for N books' categories, it makes 2 queries total: one for books, one for all related categories. |

**Why this matters:** Without these optimizations, displaying a list of 100 books could trigger hundreds or thousands of database queries. With proper optimization, it might only take 3-4 queries total, making your API dramatically faster.

### Custom Actions and Logic

1.  **`@action` Decorator**: This powerful feature allows developers to add custom, non-standard endpoints to a ViewSet.
    *   **Example (Detail Action)**: `/api/authors/{id}/books/` is exposed via `@action(detail=True, methods=['get'])` in `AuthorViewSet` to fetch a specific author's books.
    *   **Example (List Action)**: `/api/books/available/` is exposed via `@action(detail=False, methods=['get'])` in `BookViewSet` to filter all available books.
    *   **The difference:** `detail=True` actions work on a single object (need an ID), while `detail=False` actions work on the entire collection.

2.  **Dynamic Serializer Selection (`get_serializer_class`)**: The `BookViewSet` uses different serializers based on the action.
    *   If the action is `'list'`, it returns the lightweight **`BookListSerializer`** (fewer fields, faster response).
    *   For other actions (retrieve, create, update), it returns the comprehensive **`BookDetailSerializer`** (all fields, nested objects).
    *   **Why this is smart:** List views don't need every detail (which would be slow), while detail views should be comprehensive.

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

1. **ModelViewSet** - Provides all CRUD operations automatically with minimal code
2. **@action decorator** - Create custom endpoints beyond standard CRUD (e.g., `/books/bestsellers/`)
3. **get_serializer_class()** - Use different serializers for different actions (light for lists, detailed for single items)
4. **perform_create()** - Hook into object creation to add custom logic (e.g., auto-setting the current user)
5. **get_queryset()** - Dynamically filter querysets based on request parameters or user permissions
6. **select_related/prefetch_related** - Optimize database queries to prevent N+1 query problems and ensure fast API responses

**Performance tip:** Always use `select_related()` and `prefetch_related()` in your ViewSet's queryset. A well-optimized API endpoint might use only 2-3 database queries regardless of how many objects are returned, while an unoptimized one could make hundreds of queries for the same data.

---

## 7. URL Configuration and Routing

### `DefaultRouter` Efficiency

DRF's **`DefaultRouter`** is essential for simplified URL management when using ViewSets.

**Advantage (Why we do this)**: When you register a ViewSet (`router.register(r'authors', AuthorViewSet, basename='author')`), the router automatically generates all required URL patterns (list, detail, update, delete, and custom `@action` paths). This is far more efficient than manually defining paths for every standard HTTP method (GET, POST, PUT, DELETE) for every resource.

**What happens automatically:**
```python
router.register(r'books', BookViewSet, basename='book')
```
This single line creates:
- `GET /api/books/` - List all books
- `POST /api/books/` - Create a book
- `GET /api/books/{id}/` - Get a specific book
- `PUT /api/books/{id}/` - Update a book
- `PATCH /api/books/{id}/` - Partially update a book
- `DELETE /api/books/{id}/` - Delete a book
- Plus any custom `@action` endpoints you defined!

**Without the router**, you'd need to write 10-15 lines of URL patterns for each ViewSet. With the router, it's just one line.

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

After setup, you'll have these endpoints automatically generated:

**Core API Endpoints include:**

```
# Authors
GET    /api/authors/              - List all authors (with pagination)
POST   /api/authors/              - Create a new author (requires authentication)
GET    /api/authors/{id}/         - Get detailed author information
PUT    /api/authors/{id}/         - Update author (all fields, requires authentication)
PATCH  /api/authors/{id}/         - Partial update author (some fields, requires authentication)
DELETE /api/authors/{id}/         - Delete author (requires authentication)
GET    /api/authors/{id}/books/   - Custom action: Get all books by this author

# Categories
GET    /api/categories/           - List all categories
POST   /api/categories/           - Create a new category
GET    /api/categories/{id}/      - Get category details
GET    /api/categories/{id}/books/ - Custom action: Get all books in this category

# Books
GET    /api/books/                - List all books (optimized with select_related/prefetch_related)
POST   /api/books/                - Create a new book
GET    /api/books/{id}/           - Get detailed book information (with author, categories, reviews)
GET    /api/books/{id}/reviews/   - Custom action: Get all reviews for this book
GET    /api/books/available/      - Custom action: Get only available books
GET    /api/books/bestsellers/    - Custom action: Get top 10 most-reviewed books

# Reviews
GET    /api/reviews/              - List all reviews
POST   /api/reviews/              - Create a new review (user auto-set from authentication)
GET    /api/reviews/{id}/         - Get review details

# Authentication
POST   /api/token/                - Get authentication token (send username/password)
```

---

## 8. Authentication and Permissions

### Authentication Schemes

The API supports multiple authentication schemes, configured in `settings.py`. The primary method shown is **Token Authentication**, which requires generating a token associated with a user.

*   **How it works:** When a user logs in, they receive a unique token (a long random string). This token must be included in the `Authorization` header of every API request that requires authentication.
*   **Usage**: The client sends the token in the `Authorization` header: `Authorization: Token YOUR_TOKEN_HERE`.
*   **Why tokens?** Unlike session-based auth, tokens are stateless - the server doesn't need to store session data, making the API scalable and perfect for mobile apps and SPAs (Single Page Applications).

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

### Permissions and Security

**Best Practice:** Permissions define the fine-grained access control to API endpoints.

1.  **Default Permissions**: `IsAuthenticatedOrReadOnly` is set globally, meaning GET requests (Read permissions) are allowed for anyone (even unauthenticated users), but POST/PUT/DELETE requests (Write permissions) require a logged-in user.

2.  **Custom Permissions**: For complex business logic, custom permissions are created by extending `permissions.BasePermission`.
    *   **`IsReviewOwnerOrReadOnly`**: Ensures that a user can only edit or delete their *own* review (`obj.user == request.user`). Anyone can read reviews, but you can only modify your own.

| Security Consideration | Why we do this (Benefit) | Why NOT to do this (Pitfall/Security Risk) |
| :--- | :--- | :--- |
| **CORS** | Using `CORS_ALLOWED_ORIGINS` to list specific frontend domains. **Benefit:** Only trusted domains can make requests to your API, preventing unauthorized cross-origin access. | **DO NOT** use `CORS_ALLOW_ALL_ORIGINS = True` in production. This allows any website to make requests to your API, which can lead to CSRF risks, data exposure, or unauthorized data modification from malicious sites. |
| **Permissions** | Applying permissions directly to ViewSets (e.g., `permission_classes = [IsAuthenticatedOrReadOnly]`). **Benefit:** Ensures only authorized users can perform write operations, protecting your data integrity. | Neglecting to apply permissions leaves endpoints open to anonymous modification (e.g., allowing anyone to `POST` to `/api/authors/`), which could fill your database with spam or malicious data. |
| **Token Security** | Storing tokens securely on the client side and transmitting only over HTTPS. **Benefit:** Prevents token theft through network interception. | Exposing tokens in URLs or storing them in browser localStorage without proper precautions can lead to XSS attacks where malicious scripts steal tokens. |

#### Use Custom Permissions in Views

```python
from .permissions import IsReviewOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]
```

---

## 9. Advanced Features

### 9.1 Filtering, Searching, and Ordering

These features are enabled globally in `settings.py` using `DjangoFilterBackend`, `SearchFilter`, and `OrderingFilter`.

*   **Filtering**: Enabled by setting `filterset_fields` in the `BookViewSet`. Usage example: `GET /api/books/?status=available&author=1`.
    *   **How it works:** The backend examines query parameters and filters the database queryset automatically. You get exact matches for the fields you specify.
    
*   **Search**: Enabled by setting `search_fields` (e.g., `title`, `isbn`). Usage example: `GET /api/books/?search=Django`.
    *   **How it works:** Performs case-insensitive partial matches across specified fields. Searching for "Django" finds "Django for Beginners", "Two Scoops of Django", etc.
    
*   **Ordering**: Enabled automatically with `ordering_fields`. Usage example: `GET /api/books/?ordering=-price` (descending price).
    *   **Tip:** Prefix with `-` for descending order, no prefix for ascending.

Already configured in ViewSets! Usage examples:

```bash
# Filter books by status
GET /api/books/?status=available

# Filter books by author
GET /api/books/?author=1

# Search books by title
GET /api/books/?search=Django

# Order books by price (ascending)
GET /api/books/?ordering=price

# Order books by price (descending - note the minus sign)
GET /api/books/?ordering=-price

# Combine multiple filters
GET /api/books/?status=available&ordering=-price&search=Python

# Filter by multiple values (books by author 1 OR author 2)
GET /api/books/?author=1&author=2
```

### 9.2 Pagination

Pagination ensures large result sets are broken into manageable pages, improving load times and reducing server memory usage.

The default pagination is configured in settings. You can customize it:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

**Why pagination matters:** Without it, requesting `/api/books/` might return 10,000 books at once, taking minutes to load and consuming massive bandwidth. With pagination, you get 10 books per request, with links to navigate to other pages.

Usage:

```bash
# Get first page
GET /api/books/

# Get second page
GET /api/books/?page=2

# Response includes navigation:
{
  "count": 150,
  "next": "http://api.example.com/api/books/?page=3",
  "previous": "http://api.example.com/api/books/?page=1",
  "results": [...]
}
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

Throttling protects the API from excessive use or DDoS attacks by limiting the request rate per user or anonymous client.

**Why this is critical:** Without throttling, a malicious actor could make thousands of requests per second, overwhelming your server, or a buggy client application could accidentally hammer your API. Throttling ensures fair usage and system stability.

Configure in `settings.py`:

```python
REST_FRAMEWORK = {
    # ...
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',      # Anonymous users: 100 requests per day
        'user': '1000/day'      # Authenticated users: 1000 requests per day
    }
}
```

**How it works:**
- Anonymous users can make 100 requests per day
- Authenticated users can make 1000 requests per day
- If the limit is exceeded, the API returns a `429 Too Many Requests` status code
- The response includes a `Retry-After` header indicating when the client can make requests again

Custom throttle:

```python
# books/throttles.py
from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

### 9.5 View Caching

Caching dramatically improves performance for endpoints that are read often but rarely change.

*   **Implementation**: Using the `@method_decorator(cache_page(time))` wrapper from Django utilities allows caching an entire ViewSet action (like `list`).
*   **Advantage**: Reduces database load and response latency by serving content directly from the cache (e.g., Redis) for the specified duration (e.g., 15 minutes).
*   **Real-world impact:** A cached book list endpoint might respond in 10ms instead of 500ms, and handle 10x more traffic without touching the database.

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

**When to use caching:**
- ✅ List views that don't change frequently (like book catalog)
- ✅ Detail views for popular items (bestseller book pages)
- ✅ Expensive computed data (statistics, aggregations)
- ❌ User-specific data (unless using per-user cache keys)
- ❌ Data that changes frequently (like stock prices)

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

Testing is crucial for ensuring code quality and verifying that API endpoints behave as expected.

### Using `APITestCase`

DRF provides the `APITestCase` class, which extends Django's `TestCase` and sets up an `APIClient` for making mock HTTP requests.

*   **Setup**: The `setUp` method typically creates test users, generates authentication tokens (`Token.objects.create(user=self.user)`), and sets credentials on the `APIClient` using `HTTP_AUTHORIZATION`.
*   **Verification**: Tests assert the expected HTTP status codes (e.g., `status.HTTP_200_OK`, `status.HTTP_201_CREATED`, `status.HTTP_401_UNAUTHORIZED`) and inspect the structure and content of `response.data`.
*   **Why testing matters:** Automated tests catch bugs before they reach production, document how your API should behave, and give you confidence when refactoring code.

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

# Run specific test method
python manage.py test books.tests.AuthorAPITestCase.test_create_author

# Run with verbosity (shows more details)
python manage.py test --verbosity=2

# Keep the test database (useful for debugging)
python manage.py test --keepdb

# Run tests in parallel (faster for large test suites)
python manage.py test --parallel

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report in htmlcov/ directory
```

**Test-Driven Development (TDD) Workflow:**
1. Write a failing test first (test what you want to build)
2. Write minimal code to make the test pass
3. Refactor the code while keeping tests green
4. Repeat

**Best practices for API tests:**
- ✅ Test all CRUD operations (Create, Read, Update, Delete)
- ✅ Test authentication and permissions (ensure unauthorized users can't access protected endpoints)
- ✅ Test validation (ensure invalid data is rejected with appropriate error messages)
- ✅ Test edge cases (empty lists, missing fields, duplicate data)
- ✅ Test custom actions and business logic
- ✅ Use factories or fixtures for test data (avoid hardcoding)

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

A robust deployment strategy requires transitioning from development settings (SQLite, `DEBUG=True`) to production-grade services (PostgreSQL, Gunicorn).

### Production Dependencies

Beyond Django and DRF, production requires packages like:

*   **Gunicorn**: A Python WSGI HTTP server required to run the application efficiently in production. Django's development server (`runserver`) is not suitable for production - it's single-threaded and not secure.
*   **`psycopg2-binary`**: The adapter needed to connect to PostgreSQL, a production-grade database much more robust than SQLite.
*   **`python-dotenv`**: Used to securely manage environment variables (like SECRET_KEY, database credentials) without hardcoding them in code.

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

### Production Settings Checklist

| Setting | Production Value | Why (Security/Best Practice) |
| :--- | :--- | :--- |
| **`DEBUG`** | `False` | Prevents unauthorized users from seeing sensitive traceback information with file paths, variable values, and SQL queries. Debug pages can leak sensitive data and provide attack vectors. |
| **`ALLOWED_HOSTS`** | Specific domain names (e.g., `['api.example.com']`) | Prevents HTTP Host header attacks where attackers manipulate the Host header to generate malicious links or bypass security controls. |
| **`SECRET_KEY`** | Unique, random, 50+ character string stored in environment variable | Used for cryptographic signing. If leaked, attackers can forge sessions, password reset tokens, and other signed data. Must be kept secret and never committed to version control. |
| **`SSL/Cookies`** | `SECURE_SSL_REDIRECT = True`, `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True` | Enforces HTTPS communication, preventing eavesdropping and man-in-the-middle attacks. Ensures cookies are only transmitted over encrypted connections, protecting user sessions and authentication tokens. |
| **Database** | PostgreSQL instead of SQLite | PostgreSQL handles concurrent connections, larger datasets, and provides ACID guarantees. SQLite is file-based and not suitable for production with multiple users. |

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

### Docker and Containerization

Containerization provides a consistent environment across development and production. The provided `docker-compose.yml` sets up a multi-container stack, including:

*   **`db`**: PostgreSQL (for persistent data storage). Data is stored in a Docker volume so it persists even if the container is recreated.
*   **`redis`**: For caching and session management, dramatically improving API response times for frequently accessed data.
*   **`web`**: The Django application, running via Gunicorn (a production-grade WSGI server that can handle concurrent requests).
*   **`nginx`**: A reverse proxy to serve static files efficiently, handle SSL termination, and distribute traffic. Nginx is much faster than Django at serving static files (CSS, JS, images).

**Why Docker?** 
- Ensures development, staging, and production environments are identical
- "It works on my machine" becomes "it works everywhere"
- Easy to scale by running multiple web containers
- Simplified deployment - just `docker-compose up` on any server

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

Common issues often revolve around configuration errors in DRF components.

### Common Issues and Solutions

| Common Issue | Cause/Symptom | Solution Based on Source |
| :--- | :--- | :--- |
| **401 Unauthorized** | Attempting a write action (POST/PUT/DELETE) without providing a valid authentication token, or if the token is formatted incorrectly. | Ensure `TokenAuthentication` is enabled in `REST_FRAMEWORK` settings and that the header is correctly formatted: `Authorization: Token YOUR_TOKEN_HERE` (note: "Token" not "Bearer"). Verify the token exists in the database for the user. |
| **CORS Errors** | Frontend running on a different origin (port or domain) attempting to access the backend API. Browser blocks the request with CORS policy errors. | Install `django-cors-headers`, add `CorsMiddleware` to the `MIDDLEWARE` list **before** `CommonMiddleware`, and explicitly list the frontend URL in `CORS_ALLOWED_ORIGINS`. Never use `CORS_ALLOW_ALL_ORIGINS = True` in production. |
| **Slow Queries (N+1 Problem)** | Serializers accessing related fields on every iteration within a list view, causing hundreds of database queries. The Django Debug Toolbar shows excessive queries. | Use `select_related()` for ForeignKey fields and `prefetch_related()` for ManyToMany fields in the ViewSet's `queryset` definition. Example: `queryset = Book.objects.select_related('author').prefetch_related('categories')`. This reduces hundreds of queries to just 2-3. |
| **`ValidationError`** | Custom validation rules failed (e.g., email already exists, rating out of bounds). The API returns 400 Bad Request with validation errors. | Review the `validate_<field>` methods in the relevant serializer (e.g., `validate_email` in `AuthorSerializer`). Check the error message in the response to understand what validation failed. Ensure your request data meets all validation requirements. |
| **500 Internal Server Error** | Unhandled exception in view code, database connection issues, or missing environment variables. | Check Django logs for the full traceback. Ensure `DEBUG=True` in development to see detailed error pages. Verify database connection settings and that all required environment variables are set. |
| **404 Not Found** | Incorrect URL, object doesn't exist, or URL routing misconfigured. | Verify the URL pattern in `urls.py`. Check that the object ID exists in the database. Use `/api/` (with trailing slash) if `APPEND_SLASH=True` in settings. |

#### Issue: CORS Errors

```python
# Install django-cors-headers
pip install django-cors-headers

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'corsheaders',
]

# Add to MIDDLEWARE (near the top, BEFORE CommonMiddleware)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
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

# Use django-debug-toolbar to visualize queries
pip install django-debug-toolbar

# Add optimizations to your ViewSet
class BookViewSet(viewsets.ModelViewSet):
    # Before: Makes N+1 queries (one for books, N for authors)
    # queryset = Book.objects.all()
    
    # After: Makes only 2-3 queries total
    queryset = Book.objects.select_related('author', 'publisher').prefetch_related('categories')
```

**Debugging slow queries:**
1. Install django-debug-toolbar to see all queries made per request
2. Look for repeated similar queries - that's the N+1 problem
3. Add `select_related()` for foreign keys that are causing duplicates
4. Add `prefetch_related()` for many-to-many relationships
5. Re-check the toolbar - you should see far fewer queries

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

- ✅ Project setup from scratch with best practices
- ✅ Creating models with proper relationships and constraints
- ✅ Building serializers with validation and nested data
- ✅ Implementing ViewSets with database optimizations
- ✅ Configuring authentication and permissions for security
- ✅ Advanced features (filtering, pagination, caching, throttling)
- ✅ Testing and documentation strategies
- ✅ Deployment to production environments
- ✅ Best practices and troubleshooting techniques

### 🎓 Key Takeaways

**The ViewSet and Router Analogy (Remember This!):**

Think of the **`ModelViewSet`** as a **master chef** who knows how to prepare all five standard meals (CRUD operations). You don't need to teach the chef how to cook each dish - they already know! 

The **`DefaultRouter`** is the **menu publisher**; once the chef is hired (registered with `router.register()`), the router automatically publishes the entire menu (all necessary endpoints) under clear, standardized paths. You save yourself the manual work of writing out every single dish on the menu card.

This is the beauty of DRF - you write minimal code, and the framework generates a complete, RESTful API with proper HTTP methods, status codes, and URL patterns.

**Core Principles to Remember:**

1. **DRY (Don't Repeat Yourself)**: Use ModelViewSet and ModelSerializer to avoid boilerplate code
2. **Separation of Concerns**: Models handle data, Serializers handle transformation, Views handle logic, URLs handle routing
3. **Security First**: Always implement authentication, permissions, and HTTPS in production
4. **Optimize Early**: Use `select_related()` and `prefetch_related()` from the start to avoid performance issues
5. **Test Everything**: Write tests as you build features, not after

### Next Steps

1. **Expand the API** - Add more models and relationships (e.g., shopping cart, wish list)
2. **Implement Webhooks** - Notify external systems of events (new order, review posted)
3. **Add Real-time Features** - Use Django Channels for WebSockets (live notifications, chat)
4. **Integrate Third-party Services** - Payment gateways (Stripe), email services (SendGrid), cloud storage (AWS S3)
5. **Mobile App Integration** - Connect iOS/Android apps to your API using the same endpoints
6. **Microservices** - Break down into smaller, specialized services that communicate via APIs
7. **GraphQL** - Implement GraphQL alongside REST using Graphene-Django for more flexible queries

### Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **DRF Documentation**: https://www.django-rest-framework.org/
- **Two Scoops of Django**: Book on Django best practices
- **Real Python**: Tutorials and courses on Django and DRF
- **Django Community**: Join the discussion on forums and Discord
- **DRF Spectacular**: https://drf-spectacular.readthedocs.io/ for API documentation
- **Classy DRF**: http://www.cdrf.co/ - Visual reference for DRF class-based views

---

**Happy Coding! 🚀**

*Remember: Building a great API is not just about making it work - it's about making it secure, performant, well-documented, and easy to use. Django REST Framework gives you all the tools you need to achieve this.*

*If you found this guide helpful, please star the repository and share it with others!*
