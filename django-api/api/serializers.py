from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from typing import Any, Optional
from django.contrib.auth.models import User
from .models import Author, Category, Publisher, Book, Review


class AuthorSerializer(serializers.ModelSerializer):
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

    @extend_schema_field(int)
    def get_books_count(self, obj: Author) -> int:
        """Return the total number of books associated with the author."""
        return obj.books.count()

    def validate_email(self, value: str) -> str:
        """Ensure email uniqueness across all authors."""
        if Author.objects.filter(email=value).exists():
            if not self.instance or self.instance.email != value:
                raise serializers.ValidationError(
                    "An author with this email already exists."
                )
        return value


class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'books_count', 'created_at']
        read_only_fields = ['created_at']

    @extend_schema_field(int)
    def get_books_count(self, obj: Category) -> int:
        """Return the number of books in this category."""
        return obj.books.count()


class PublisherSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Publisher
        fields = [
            'id', 'name', 'address', 'city', 'country',
            'website', 'books_count', 'created_at'
        ]
        read_only_fields = ['created_at']

    @extend_schema_field(int)
    def get_books_count(self, obj: Publisher) -> int:
        """Return the number of books published by this publisher."""
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    categories = serializers.StringRelatedField(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author_name', 'categories',
            'price', 'status', 'average_rating', 'publication_date'
        ]

    @extend_schema_field(float)
    def get_average_rating(self, obj: Book) -> Optional[float]:
        """Calculate the average rating from all reviews."""
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None


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

    @extend_schema_field(int)
    def get_reviews_count(self, obj: Book) -> int:
        """Return total number of reviews for the book."""
        return obj.reviews.count()

    @extend_schema_field(float)
    def get_average_rating(self, obj: Book) -> Optional[float]:
        """Return average rating rounded to 2 decimal places."""
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return None


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