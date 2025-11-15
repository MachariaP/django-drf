from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from typing import Any, Optional
from django.contrib.auth.models import User
from .models import Author, Category, Publisher, Book, Review


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'birth_date', 'biography', 'email', 'website',
            'books_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_email(self, value: str) -> str:
        """Ensure email uniqueness across all authors."""
        if Author.objects.filter(email=value).exists():
            if not self.instance or self.instance.email != value:
                raise serializers.ValidationError(
                    "An author with this email already exists."
                )
        return value


class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'books_count', 'created_at']
        read_only_fields = ['created_at']


class PublisherSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Publisher
        fields = [
            'id', 'name', 'address', 'city', 'country',
            'website', 'books_count', 'created_at'
        ]
        read_only_fields = ['created_at']


class BookListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    categories = serializers.StringRelatedField(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author_name', 'categories',
            'price', 'status', 'average_rating', 'publication_date'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
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
    reviews_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

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


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'book', 'book_title', 'user', 'rating',
            'title', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_rating(self, value: int) -> int:
        """Ensure the rating is an integer between 1 and 5 inclusive."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data: dict) -> Review:
        """Automatically assign the authenticated user to the review."""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'reviews_count']
        read_only_fields = ['id']

    @extend_schema_field(int)
    def get_reviews_count(self, obj: User) -> int:
        """Return the total number of reviews written by the user."""
        return obj.reviews.count()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with Django's built-in password validation.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Password must be at least 8 characters long'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Re-enter password for confirmation'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate_email(self, value: str) -> str:
        """Ensure email uniqueness."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, attrs: dict) -> dict:
        """Validate password match and strength using Django validators."""
        from django.contrib.auth.password_validation import validate_password
        
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        
        # Check password match
        if password != password_confirm:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        
        # Validate password using Django's built-in validators
        try:
            validate_password(password, user=User(**attrs))
        except Exception as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return attrs
    
    def create(self, validated_data: dict) -> User:
        """Create user with hashed password."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login using Django's authentication.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs: dict) -> dict:
        """Authenticate user credentials."""
        from django.contrib.auth import authenticate
        
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        
        attrs['user'] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value: str) -> str:
        """Verify old password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
    
    def validate(self, attrs: dict) -> dict:
        """Validate new password match and strength."""
        from django.contrib.auth.password_validation import validate_password
        
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        
        if new_password != new_password_confirm:
            raise serializers.ValidationError({'new_password_confirm': 'Passwords do not match.'})
        
        # Validate new password using Django's validators
        try:
            validate_password(new_password, user=self.context['request'].user)
        except Exception as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        return attrs
    
    def save(self):
        """Update user password."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user