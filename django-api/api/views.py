from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from django.db import connection

from api.pagination import StandardResultsSetPagination
from .models import Author, Category, Publisher, Book, Review
from .serializers import (
    AuthorSerializer, CategorySerializer, PublisherSerializer,
    BookListSerializer, BookDetailSerializer, ReviewSerializer, UserSerializer
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


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring and deployment platforms.
    
    Returns:
        - 200 OK if the application is running and database is accessible
        - 503 Service Unavailable if database connection fails
    
    Example: GET /api/health/
    """
    try:
        # Check database connectivity
        connection.ensure_connection()
        
        return Response({
            'status': 'healthy',
            'database': 'connected',
            'api': 'running'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    User registration endpoint.
    
    Creates a new user account and returns authentication token.
    
    Request body:
        - username (required): Unique username
        - email (required): Email address
        - password (required): Password (min 8 characters)
        - first_name (optional): First name
        - last_name (optional): Last name
    
    Returns:
        - 201 Created: User created successfully with token
        - 400 Bad Request: Validation errors
    
    Example: POST /api/register/
    """
    from rest_framework.authtoken.models import Token
    
    # Validate required fields
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not email or not password:
        return Response({
            'error': 'Username, email, and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response({
            'error': 'Username already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email already exists
    if User.objects.filter(email=email).exists():
        return Response({
            'error': 'Email already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate password length
    if len(password) < 8:
        return Response({
            'error': 'Password must be at least 8 characters long'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=request.data.get('first_name', ''),
            last_name=request.data.get('last_name', '')
        )
        
        # Create token for the user
        token = Token.objects.create(user=user)
        
        # Serialize user data
        serializer = UserSerializer(user)
        
        return Response({
            'user': serializer.data,
            'token': token.key,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Error creating user: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
