from rest_framework import serializers
from .models import Author, Category, Publisher, Book, Review
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Provides serialization for all author fields, including:
    - Computed `full_name` (read-only)
    - `books_count` via SerializerMethodField
    - Custom email uniqueness validation
    """
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
        """
        Return the total number of books associated with the author.
        """
        return obj.books.count()

    def validate_email(self, value):
        """
        Ensure email uniqueness across all authors.
        Allows update if the email belongs to the current instance.
        """
        if Author.objects.filter(email=value).exists():
            if not self.instance or self.instance.email != value:
                raise serializers.ValidationError(
                    "An author with this email already exists."
                )
        return value


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Includes:
    - `books_count` to show how many books belong to the category
    """
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'books_count', 'created_at']
        read_only_fields = ['created_at']

    def get_books_count(self, obj):
        """
        Return the number of books in this category.
        """
        return obj.books.count()


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Publisher model.

    Includes:
    - `books_count` to indicate how many books the publisher has
    """
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Publisher
        fields = [
            'id', 'name', 'address', 'city', 'country',
            'website', 'books_count', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_books_count(self, obj):
        """
        Return the number of books published by this publisher.
        """
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for Book model used in list views.

    Optimized for performance:
    - Uses `author.full_name` via `source`
    - `categories` as string representation (no nested serialization)
    - `average_rating` computed from reviews
    """
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
        """
        Calculate the average rating from all reviews.
        Returns `None` if no reviews exist.
        """
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Book model used in retrieve/update views.

    Features:
    - Nested read-only serializers for `author`, `categories`, `publisher`
    - Write-only `*_id` fields for creating/updating relationships
    - `reviews_count` and rounded `average_rating`
    """
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
        """
        Return total number of reviews for the book.
        """
        return obj.reviews.count()

    def get_average_rating(self, obj):
        """
        Return average rating rounded to 2 decimal places.
        Returns `None` if no reviews.
        """
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return None


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Features:
    - `user` shown as string (username)
    - `book_title` for context in responses
    - Auto-assigns current user on create
    - Validates rating is between 1 and 5
    """
    user = serializers.StringRelatedField(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'book', 'book_title', 'user', 'rating',
            'title', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated  ']

    def validate_rating(self, value):
        """
        Ensure the rating is an integer between 1 and 5 inclusive.
        """
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        """
        Automatically assign the authenticated user to the review.
        Uses `request.user` from serializer context.
        """
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Django User model.

    Includes:
    - `reviews_count` to show how many reviews the user has written
    """
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'reviews_count']
        read_only_fields = ['id']

    def get_reviews_count(self, obj):
        """
        Return the total number of reviews written by the user.
        """
        return obj.reviews.count()
