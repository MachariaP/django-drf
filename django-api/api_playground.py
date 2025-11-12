#!/usr/bin/env python
"""
Django REST Framework API Playground Script
============================================

This interactive script helps you test and explore your API endpoints.
It provides commands to:
- List, create, update, and delete books, authors, categories, publishers
- Add and view reviews
- Search and filter books
- Test authentication and permissions
- View API statistics

Usage:
    python api_playground.py

Requirements:
    - Django server must be running (python manage.py runserver)
    - You must have created a superuser (python manage.py createsuperuser)
    - Sample data loaded (python seed_books.py)
"""

import os
import sys
import json
import requests
from getpass import getpass
from datetime import date

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

# Global token storage
AUTH_TOKEN = None
SESSION = requests.Session()


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_json(data, indent=2):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=indent))


def get_auth_token(username=None, password=None):
    """Authenticate and get token."""
    global AUTH_TOKEN
    
    if not username:
        print("\n🔐 Authentication Required")
        username = input("Username: ")
    if not password:
        password = getpass("Password: ")
    
    try:
        response = requests.post(
            f"{BASE_URL.replace('/api', '')}/api/token/",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            AUTH_TOKEN = response.json()["token"]
            SESSION.headers.update({"Authorization": f"Token {AUTH_TOKEN}"})
            print(f"✅ Authenticated successfully as {username}")
            return True
        else:
            print(f"❌ Authentication failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def list_books(search=None, status=None, page=1):
    """List all books with optional filters."""
    print_header("📚 Books List")
    
    params = {"page": page}
    if search:
        params["search"] = search
    if status:
        params["status"] = status
    
    try:
        response = SESSION.get(f"{BASE_URL}/books/", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"\nTotal: {data.get('count', 0)} books")
            print(f"Page {page} of {(data.get('count', 0) + 9) // 10}\n")
            
            for book in data.get('results', []):
                print(f"[{book['id']}] {book['title']}")
                print(f"    Author: {book.get('author_name', 'Unknown')}")
                print(f"    Price: ${book['price']} | Status: {book['status']}")
                rating = book.get('average_rating')
                if rating:
                    print(f"    Rating: {rating:.1f}⭐")
                print()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def get_book_detail(book_id):
    """Get detailed information about a book."""
    print_header(f"📖 Book Details (ID: {book_id})")
    
    try:
        response = SESSION.get(f"{BASE_URL}/books/{book_id}/")
        if response.status_code == 200:
            book = response.json()
            print(f"\nTitle: {book['title']}")
            if book.get('subtitle'):
                print(f"Subtitle: {book['subtitle']}")
            print(f"ISBN: {book['isbn']}")
            print(f"Author: {book['author']['first_name']} {book['author']['last_name']}")
            print(f"Publisher: {book.get('publisher', {}).get('name', 'N/A')}")
            print(f"Publication Date: {book['publication_date']}")
            print(f"Pages: {book['pages']}")
            print(f"Price: ${book['price']}")
            print(f"Status: {book['status']}")
            
            categories = [cat['name'] for cat in book.get('categories', [])]
            if categories:
                print(f"Categories: {', '.join(categories)}")
            
            print(f"\nReviews: {book.get('reviews_count', 0)}")
            avg_rating = book.get('average_rating')
            if avg_rating:
                print(f"Average Rating: {avg_rating}⭐")
            
            if book.get('description'):
                print(f"\nDescription:\n{book['description']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def create_book():
    """Interactive book creation."""
    print_header("➕ Create New Book")
    
    if not AUTH_TOKEN:
        print("❌ You must be authenticated to create a book")
        return
    
    print("\nEnter book details:")
    title = input("Title: ")
    isbn = input("ISBN (13 digits): ")
    
    # List authors to choose from
    response = SESSION.get(f"{BASE_URL}/authors/")
    if response.status_code == 200:
        authors = response.json().get('results', [])
        print("\nAvailable Authors:")
        for author in authors[:10]:
            print(f"[{author['id']}] {author['full_name']}")
        author_id = int(input("\nAuthor ID: "))
    else:
        print("❌ Could not fetch authors")
        return
    
    publication_date = input("Publication Date (YYYY-MM-DD): ")
    pages = int(input("Number of Pages: "))
    price = float(input("Price: "))
    description = input("Description (optional): ")
    
    book_data = {
        "title": title,
        "isbn": isbn,
        "author_id": author_id,
        "publication_date": publication_date,
        "pages": pages,
        "price": price,
        "description": description,
        "status": "available"
    }
    
    try:
        response = SESSION.post(f"{BASE_URL}/books/", json=book_data)
        if response.status_code == 201:
            book = response.json()
            print(f"\n✅ Book created successfully! ID: {book['id']}")
            print_json(book)
        else:
            print(f"❌ Error: {response.status_code}")
            print_json(response.json())
    except Exception as e:
        print(f"❌ Error: {e}")


def list_authors(page=1):
    """List all authors."""
    print_header("👥 Authors List")
    
    try:
        response = SESSION.get(f"{BASE_URL}/authors/", params={"page": page})
        if response.status_code == 200:
            data = response.json()
            print(f"\nTotal: {data.get('count', 0)} authors\n")
            
            for author in data.get('results', []):
                print(f"[{author['id']}] {author['full_name']}")
                print(f"    Email: {author['email']}")
                print(f"    Books: {author.get('books_count', 0)}")
                if author.get('website'):
                    print(f"    Website: {author['website']}")
                print()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def get_author_books(author_id):
    """Get all books by a specific author."""
    print_header(f"📚 Books by Author (ID: {author_id})")
    
    try:
        response = SESSION.get(f"{BASE_URL}/authors/{author_id}/books/")
        if response.status_code == 200:
            books = response.json()
            print(f"\nFound {len(books)} books:\n")
            
            for book in books:
                print(f"[{book['id']}] {book['title']}")
                print(f"    Price: ${book['price']} | Status: {book['status']}")
                print()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def list_categories():
    """List all categories."""
    print_header("🏷️  Categories")
    
    try:
        response = SESSION.get(f"{BASE_URL}/categories/")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('results', [])
            print(f"\nTotal: {data.get('count', 0)} categories\n")
            
            for cat in categories:
                print(f"[{cat['id']}] {cat['name']}")
                print(f"    Books: {cat.get('books_count', 0)}")
                if cat.get('description'):
                    print(f"    {cat['description']}")
                print()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def add_review(book_id):
    """Add a review to a book."""
    print_header(f"⭐ Add Review for Book #{book_id}")
    
    if not AUTH_TOKEN:
        print("❌ You must be authenticated to add a review")
        return
    
    rating = int(input("Rating (1-5): "))
    if not 1 <= rating <= 5:
        print("❌ Rating must be between 1 and 5")
        return
    
    title = input("Review Title: ")
    comment = input("Comment: ")
    
    review_data = {
        "book": book_id,
        "rating": rating,
        "title": title,
        "comment": comment
    }
    
    try:
        response = SESSION.post(f"{BASE_URL}/reviews/", json=review_data)
        if response.status_code == 201:
            print("\n✅ Review added successfully!")
            print_json(response.json())
        else:
            print(f"❌ Error: {response.status_code}")
            print_json(response.json())
    except Exception as e:
        print(f"❌ Error: {e}")


def get_book_reviews(book_id):
    """Get all reviews for a book."""
    print_header(f"📝 Reviews for Book #{book_id}")
    
    try:
        response = SESSION.get(f"{BASE_URL}/books/{book_id}/reviews/")
        if response.status_code == 200:
            reviews = response.json()
            print(f"\nFound {len(reviews)} reviews:\n")
            
            for review in reviews:
                print(f"⭐ {review['rating']}/5 - {review['title']}")
                print(f"   By: {review['user']}")
                print(f"   {review['comment']}")
                print(f"   Posted: {review['created_at']}")
                print()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def search_books():
    """Search books interactively."""
    print_header("🔍 Search Books")
    
    query = input("\nEnter search term: ")
    list_books(search=query)


def get_bestsellers():
    """Get bestselling books (most reviewed)."""
    print_header("🏆 Bestsellers")
    
    try:
        response = SESSION.get(f"{BASE_URL}/books/bestsellers/")
        if response.status_code == 200:
            books = response.json()
            print(f"\nTop {len(books)} bestselling books:\n")
            
            for i, book in enumerate(books, 1):
                print(f"{i}. [{book['id']}] {book['title']}")
                print(f"   Author: {book.get('author_name', 'Unknown')}")
                print(f"   Price: ${book['price']}")
                rating = book.get('average_rating')
                if rating:
                    print(f"   Rating: {rating:.1f}⭐")
                print()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def show_api_stats():
    """Display API statistics."""
    print_header("📊 API Statistics")
    
    try:
        # Get counts for each model
        books_resp = SESSION.get(f"{BASE_URL}/books/")
        authors_resp = SESSION.get(f"{BASE_URL}/authors/")
        categories_resp = SESSION.get(f"{BASE_URL}/categories/")
        reviews_resp = SESSION.get(f"{BASE_URL}/reviews/")
        
        if all(r.status_code == 200 for r in [books_resp, authors_resp, categories_resp, reviews_resp]):
            print("\nDatabase Statistics:")
            print(f"  📚 Books: {books_resp.json().get('count', 0)}")
            print(f"  👥 Authors: {authors_resp.json().get('count', 0)}")
            print(f"  🏷️  Categories: {categories_resp.json().get('count', 0)}")
            print(f"  ⭐ Reviews: {reviews_resp.json().get('count', 0)}")
            print()
        else:
            print("❌ Error fetching statistics")
    except Exception as e:
        print(f"❌ Error: {e}")


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 70)
    print("  📚 Django REST Framework API Playground")
    print("=" * 70)
    print("\n📖 BOOKS")
    print("  1. List all books")
    print("  2. View book details")
    print("  3. Create new book")
    print("  4. Search books")
    print("  5. Get bestsellers")
    print("\n👥 AUTHORS")
    print("  6. List all authors")
    print("  7. Get author's books")
    print("\n🏷️  CATEGORIES")
    print("  8. List all categories")
    print("\n⭐ REVIEWS")
    print("  9. Add review to book")
    print("  10. View book reviews")
    print("\n🔧 UTILITIES")
    print("  11. Show API statistics")
    print("  12. Re-authenticate")
    print("\n  0. Exit")
    print("=" * 70)


def main():
    """Main program loop."""
    print("\n" + "=" * 70)
    print("  Welcome to Django REST Framework API Playground!")
    print("=" * 70)
    print("\nThis script helps you interact with your API endpoints.")
    print("Make sure your Django server is running on http://127.0.0.1:8000")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/books/", timeout=2)
        print("✅ API server is reachable")
    except:
        print("❌ Cannot reach API server. Make sure it's running:")
        print("   python manage.py runserver")
        return
    
    # Authenticate
    print("\nYou can browse without authentication, but creating/editing requires login.")
    choice = input("Authenticate now? (y/n): ").lower()
    if choice == 'y':
        get_auth_token()
    
    # Main loop
    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == '0':
                print("\n👋 Goodbye!")
                break
            elif choice == '1':
                page = int(input("Page number (default 1): ") or "1")
                list_books(page=page)
            elif choice == '2':
                book_id = int(input("Enter book ID: "))
                get_book_detail(book_id)
            elif choice == '3':
                create_book()
            elif choice == '4':
                search_books()
            elif choice == '5':
                get_bestsellers()
            elif choice == '6':
                page = int(input("Page number (default 1): ") or "1")
                list_authors(page=page)
            elif choice == '7':
                author_id = int(input("Enter author ID: "))
                get_author_books(author_id)
            elif choice == '8':
                list_categories()
            elif choice == '9':
                book_id = int(input("Enter book ID: "))
                add_review(book_id)
            elif choice == '10':
                book_id = int(input("Enter book ID: "))
                get_book_reviews(book_id)
            elif choice == '11':
                show_api_stats()
            elif choice == '12':
                get_auth_token()
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
