from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Author, Category, Publisher, Book, Review


@admin.register(Author)
#class AuthorAdmin(admin.ModelAdmin):
class AuthorAdmin(ImportExportModelAdmin):
    """
    Admin interface for the Author model.

    Displays author's full name, email, and creation date.
    Enables searching by first name, last name, and email,
    and filtering by creation date.
    """
    list_display = ['full_name', 'email', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['created_at']


@admin.register(Category)
#class CategoryAdmin(admin.ModelAdmin):
class CategoryAdmin(ImportExportModelAdmin):
    """
    Admin interface for the Category model.

    Displays category name, slug, and creation date.
    Enables searching by name and slug.
    """
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Publisher)
#class PublisherAdmin(admin.ModelAdmin):
class PublisherAdmin(ImportExportModelAdmin):
    """
    Admin interface for the Publisher model.

    Displays publisher name, city, and country.
    Enables searching by name, city, and country.
    """
    list_display = ['name', 'city', 'country']
    search_fields = ['name', 'city', 'country']


@admin.register(Book)
#class BookAdmin(admin.ModelAdmin):
class BookAdmin(ImportExportModelAdmin):
    """
    Admin interface for the Book model.

    Displays book title, author, publisher, status, price, and publication date.
    Enables filtering by status, publication date, and categories.
    Supports searching by title, ISBN, and author's name.
    Allows horizontal filtering for categories and provides a date hierarchy on publication date.
    """
    list_display = ['title', 'author', 'publisher', 'status', 'price', 'publication_date']
    list_filter = ['status', 'publication_date', 'categories']
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']
    filter_horizontal = ['categories']
    date_hierarchy = 'publication_date'


@admin.register(Review)
#class ReviewAdmin(admin.ModelAdmin):
class ReviewAdmin(ImportExportModelAdmin):
    """
    Admin interface for the Review model.

    Displays review title, book, user, rating, and creation date.
    Enables filtering by rating and creation date.
    Supports searching by book title, user username, and review title.
    """
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'title']
