from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    """
    Model representing an author.

    Stores personal information about book authors including name, birth date,
    biography, contact details, and timestamps for record creation and updates.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Author model."""
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'Authors'

    def __str__(self):
        """Return the full name of the author."""
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        """
        Property that returns the author's full name.

        Useful in templates or serializers where method-style attribute is preferred.
        """
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    """
    Model representing a book category (e.g., Fiction, Science, History).

    Categories help organize books and enable filtering by genre or subject matter.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Category model."""
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        """Return the name of the category."""
        return self.name


class Publisher(models.Model):
    """
    Model representing a book publisher.

    Stores publisher details such as name, address, website, and timestamps.
    """
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Publisher model."""
        ordering = ['name']

    def __str__(self):
        """Return the name of the publisher."""
        return self.name


class Book(models.Model):
    """
    Model representing a book in the catalog.

    Contains comprehensive book metadata including title, author, categories,
    publisher, publication date, ISBN, number of pages, price, description, cover image,
    availability status, and timestamps for creation and updates.
    """
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
        """Meta options for the Book model."""
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
        ]

    def __str__(self):
        """Return the title of the book."""
        return self.title


class Review(models.Model):
    """
    Model representing a book review.
    
    Stores user-generated reviews for books, including rating, title, comment,
    and timestamps for creation and updates.
    """
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
        """Meta options for the Review model."""
        ordering = ['-created_at']
        unique_together = ['book', 'user']  # One review per user per book

    def __str__(self):
        """Return a string representation of the review."""
        return f"{self.user.username}'s review of {self.book.title}"