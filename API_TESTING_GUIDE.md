# 🎮 API Testing & Playground Guide

This guide shows you how to test and interact with your Django REST Framework API.

## 📋 Prerequisites

Before testing, make sure you have:

1. ✅ Installed all dependencies: `pip install -r requirements.txt`
2. ✅ Run migrations: `python manage.py migrate`
3. ✅ Created a superuser: `python manage.py createsuperuser`
4. ✅ Seeded sample data: `python seed_books.py`
5. ✅ Started the server: `python manage.py runserver`

## 🚀 Method 1: Interactive Python Playground (Recommended)

The interactive Python playground provides a menu-driven interface to explore all API endpoints.

### Usage:

```bash
cd django-api
python api_playground.py
```

### Features:

- 📚 **Books Management**
  - List all books with pagination
  - View detailed book information
  - Create new books
  - Search books by title, ISBN, or description
  - Get bestsellers (most reviewed books)

- 👥 **Authors Management**
  - List all authors
  - View author details
  - See all books by a specific author

- 🏷️ **Categories**
  - List all book categories
  - View books in each category

- ⭐ **Reviews**
  - Add reviews to books
  - View all reviews for a book
  - See average ratings

- 🔧 **Utilities**
  - API statistics (total books, authors, categories, reviews)
  - Re-authentication

### Example Session:

```
📚 Django REST Framework API Playground
========================================

1. List all books
2. View book details
3. Create new book
4. Search books
...

Enter your choice: 1

📚 Books List
Total: 24 books
Page 1 of 3

[24] Grokking Algorithms
    Author: Aditya Bhargava
    Price: $29.99 | Status: available
    Rating: 3.5⭐
```

## 🔧 Method 2: Shell Script (Quick Testing)

For quick command-line testing, use the bash script:

```bash
cd django-api
./test_api.sh
```

This script tests all major endpoints and displays formatted JSON responses.

## 🌐 Method 3: Web Browser

### Browsable API

Django REST Framework provides a beautiful web interface:

1. Start your server: `python manage.py runserver`
2. Visit: http://127.0.0.1:8000/api/
3. Navigate through endpoints using your browser

### API Documentation

Access auto-generated interactive documentation:

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

## 🔐 Authentication

The API provides comprehensive authentication endpoints using Django's built-in secure authentication system.

### Registration

Register a new user account:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

Response:
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "reviews_count": 0
  },
  "token": "your_authentication_token_here",
  "message": "User registered successfully"
}
```

### Login

Login with username and password:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "reviews_count": 0
  },
  "token": "your_authentication_token_here",
  "message": "Login successful"
}
```

### Using Authentication Token

Use the token in requests to access protected endpoints:

```bash
curl -X GET http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get User Profile

Get current user's profile:

```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Change Password

Change password for authenticated user:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/change-password/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password_confirm": "NewSecurePass456!"
  }'
```

### Logout

Logout and invalidate authentication token:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Legacy Token Endpoint (Still Available)

You can also get a token using the legacy endpoint:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -d "username=admin&password=admin123"
```

## 📝 Available Endpoints

### Authentication
```
POST   /api/auth/register/        - Register a new user
POST   /api/auth/login/           - Login and get token
POST   /api/auth/logout/          - Logout and invalidate token
POST   /api/auth/change-password/ - Change password
GET    /api/auth/profile/         - Get current user profile
POST   /api/token/                - Get token (legacy)
```

### Books
```
GET    /api/books/              - List all books
POST   /api/books/              - Create a book
GET    /api/books/{id}/         - Get book details
PUT    /api/books/{id}/         - Update book
PATCH  /api/books/{id}/         - Partial update
DELETE /api/books/{id}/         - Delete book
GET    /api/books/available/    - Get available books only
GET    /api/books/bestsellers/  - Get top 10 bestsellers
GET    /api/books/{id}/reviews/ - Get reviews for a book
```

### Authors
```
GET    /api/authors/            - List all authors
POST   /api/authors/            - Create an author
GET    /api/authors/{id}/       - Get author details
GET    /api/authors/{id}/books/ - Get books by author
```

### Categories
```
GET    /api/categories/         - List all categories
POST   /api/categories/         - Create a category
GET    /api/categories/{id}/    - Get category details
GET    /api/categories/{id}/books/ - Get books in category
```

### Publishers
```
GET    /api/publishers/         - List all publishers
POST   /api/publishers/         - Create a publisher
GET    /api/publishers/{id}/    - Get publisher details
```

### Reviews
```
GET    /api/reviews/            - List all reviews
POST   /api/reviews/            - Create a review
GET    /api/reviews/{id}/       - Get review details
```

## 🔍 Query Parameters

### Filtering
```bash
# Filter books by status
GET /api/books/?status=available

# Filter books by author
GET /api/books/?author=1

# Filter books by category
GET /api/books/?categories=3
```

### Searching
```bash
# Search in title, subtitle, ISBN, description
GET /api/books/?search=python

# Search authors by name
GET /api/authors/?search=martin
```

### Ordering
```bash
# Order by price (ascending)
GET /api/books/?ordering=price

# Order by price (descending)
GET /api/books/?ordering=-price

# Multiple ordering
GET /api/books/?ordering=-created_at,title
```

### Pagination
```bash
# Get page 2
GET /api/books/?page=2

# Custom page size
GET /api/books/?page_size=20
```

### Combining Filters
```bash
# Available Python books, ordered by price
GET /api/books/?status=available&search=python&ordering=price
```

## 🧪 Testing with cURL

### Create a Book
```bash
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Book",
    "isbn": "9781234567890",
    "author_id": 1,
    "publication_date": "2024-01-01",
    "pages": 300,
    "price": 29.99,
    "description": "An amazing book!",
    "status": "available"
  }'
```

### Update a Book
```bash
curl -X PATCH http://127.0.0.1:8000/api/books/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price": 24.99}'
```

### Add a Review
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "rating": 5,
    "title": "Excellent!",
    "comment": "This book changed my life!"
  }'
```

## 🐍 Testing with Python Requests

```python
import requests

# Base URL
BASE_URL = "http://127.0.0.1:8000/api"

# Get token
response = requests.post(
    f"{BASE_URL.replace('/api', '')}/api/token/",
    data={"username": "admin", "password": "admin123"}
)
token = response.json()["token"]

# Set headers
headers = {"Authorization": f"Token {token}"}

# List books
books = requests.get(f"{BASE_URL}/books/", headers=headers).json()
print(f"Total books: {books['count']}")

# Get book details
book = requests.get(f"{BASE_URL}/books/1/", headers=headers).json()
print(f"Book: {book['title']} by {book['author']['full_name']}")

# Create a review
review_data = {
    "book": 1,
    "rating": 5,
    "title": "Great!",
    "comment": "Loved it!"
}
review = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=headers).json()
print(f"Review created: {review['id']}")
```

## 🔥 Quick Start Commands

```bash
# Setup (one-time)
cd django-api
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python seed_books.py

# Start development
python manage.py runserver

# In another terminal - Test the API
python api_playground.py

# Or use the shell script
./test_api.sh

# Or visit in browser
# http://127.0.0.1:8000/api/docs/
```

## 💡 Tips

1. **Use the interactive playground** (`api_playground.py`) for exploring and learning the API
2. **Use the browsable API** in your browser for quick manual testing
3. **Use cURL or requests** for automated testing and scripting
4. **Check API documentation** at `/api/docs/` for detailed endpoint information
5. **Run Django tests** with `python manage.py test` to ensure everything works

## 🆘 Troubleshooting

### "Cannot reach API server"
- Make sure Django server is running: `python manage.py runserver`
- Check the server is on http://127.0.0.1:8000

### "401 Unauthorized"
- You need to authenticate for write operations (POST/PUT/DELETE)
- Get a token using `/api/auth/login/` or `/api/auth/register/` endpoint
- Include token in header: `Authorization: Token YOUR_TOKEN`

### "404 Not Found"
- Check the endpoint URL is correct
- Ensure the object ID exists in the database

### "No data available"
- Run the seed script: `python seed_books.py`

### "Password validation errors"
- Passwords must be at least 8 characters long
- Passwords cannot be too similar to your username or email
- Passwords cannot be entirely numeric
- Passwords cannot be too common (e.g., "password123")
- Use strong passwords with a mix of characters

### "Token is invalid after password change"
- This is expected behavior for security
- A new token is issued when you change your password
- Use the new token returned in the response

---

## 🔒 Security Notes

- All passwords are securely hashed using Django's built-in password hashing (PBKDF2)
- Passwords are validated using Django's password validators
- Tokens are invalidated on logout and password change
- Use HTTPS in production to protect authentication tokens
- Never share your authentication token
- Store tokens securely on the client side

---

Happy API Testing! 🚀

For more information, see the main [guide.md](../guide.md) file.
