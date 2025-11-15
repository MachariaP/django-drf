# 🧪 API Testing Guide - Quick Reference

This guide provides quick examples for testing your deployed Django REST Framework API.

---

## Base URL

Replace `YOUR_SERVICE_NAME` with your actual Render service name:

```
https://YOUR_SERVICE_NAME.onrender.com
```

For local testing:
```
http://localhost:8000
```

---

## 1. Health Check

Test if the API is running and database is connected.

**Request:**
```bash
curl https://YOUR_SERVICE_NAME.onrender.com/api/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "api": "running"
}
```

---

## 2. Register a New User

Create a new user account and receive an authentication token.

**Request:**
```bash
curl -X POST https://YOUR_SERVICE_NAME.onrender.com/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Expected Response:**
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
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "message": "User created successfully"
}
```

**Save your token!** You'll need it for authenticated requests.

---

## 3. Login (Get Token)

For existing users, get a new authentication token.

**Request:**
```bash
curl -X POST https://YOUR_SERVICE_NAME.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

**Expected Response:**
```json
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
}
```

---

## 4. List Books (Public)

View all available books (no authentication required for read operations).

**Request:**
```bash
curl https://YOUR_SERVICE_NAME.onrender.com/api/books/
```

**Expected Response:**
```json
{
  "count": 10,
  "next": "https://YOUR_SERVICE_NAME.onrender.com/api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author_name": "F. Scott Fitzgerald",
      "categories": ["Fiction", "Classic"],
      "price": "12.99",
      "status": "available",
      "average_rating": 4.5,
      "publication_date": "1925-04-10"
    }
  ]
}
```

---

## 5. Create a Book (Authenticated)

Create a new book (requires authentication token).

**Request:**
```bash
curl -X POST https://YOUR_SERVICE_NAME.onrender.com/api/books/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Book",
    "subtitle": "An Amazing Story",
    "isbn": "9781234567890",
    "author_id": 1,
    "category_ids": [1, 2],
    "publisher_id": 1,
    "publication_date": "2024-01-15",
    "pages": 350,
    "price": "24.99",
    "description": "An incredible journey through...",
    "status": "available"
  }'
```

**Expected Response:**
```json
{
  "id": 11,
  "title": "My New Book",
  "subtitle": "An Amazing Story",
  "isbn": "9781234567890",
  "author": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    ...
  },
  ...
}
```

---

## 6. List Authors

**Request:**
```bash
curl https://YOUR_SERVICE_NAME.onrender.com/api/authors/
```

---

## 7. Create an Author (Authenticated)

**Request:**
```bash
curl -X POST https://YOUR_SERVICE_NAME.onrender.com/api/authors/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Austen",
    "email": "jane.austen@example.com",
    "biography": "English novelist known for her romantic fiction",
    "birth_date": "1775-12-16"
  }'
```

---

## 8. Create a Review (Authenticated)

Post a review for a book.

**Request:**
```bash
curl -X POST https://YOUR_SERVICE_NAME.onrender.com/api/reviews/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "rating": 5,
    "title": "Excellent book!",
    "comment": "I absolutely loved this book. The characters were well-developed and the plot was engaging."
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "book": 1,
  "book_title": "The Great Gatsby",
  "user": "johndoe",
  "rating": 5,
  "title": "Excellent book!",
  "comment": "I absolutely loved this book...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

## 9. Search Books

Search for books by title, subtitle, ISBN, or description.

**Request:**
```bash
curl "https://YOUR_SERVICE_NAME.onrender.com/api/books/?search=gatsby"
```

---

## 10. Filter Books

Filter books by status, author, category, or publisher.

**Request:**
```bash
# Filter by status
curl "https://YOUR_SERVICE_NAME.onrender.com/api/books/?status=available"

# Filter by author
curl "https://YOUR_SERVICE_NAME.onrender.com/api/books/?author=1"

# Filter by category
curl "https://YOUR_SERVICE_NAME.onrender.com/api/books/?categories=2"

# Combine filters
curl "https://YOUR_SERVICE_NAME.onrender.com/api/books/?status=available&author=1"
```

---

## 11. Get Bestsellers

Get the top 10 most-reviewed books.

**Request:**
```bash
curl https://YOUR_SERVICE_NAME.onrender.com/api/books/bestsellers/
```

---

## 12. Get Available Books

Get only books with "available" status.

**Request:**
```bash
curl https://YOUR_SERVICE_NAME.onrender.com/api/books/available/
```

---

## Using Postman

1. **Import the API:**
   - Open Postman
   - Go to your service URL + `/api/schema/`
   - Import the OpenAPI schema

2. **Set up Authentication:**
   - In Postman, go to "Authorization" tab
   - Select "API Key"
   - Key: `Authorization`
   - Value: `Token YOUR_TOKEN_HERE`
   - Add to: Header

3. **Test endpoints** using the visual interface

---

## Using Swagger UI (Interactive Docs)

Visit your API documentation at:
```
https://YOUR_SERVICE_NAME.onrender.com/api/docs/
```

1. Click on any endpoint to expand it
2. Click "Try it out"
3. For authenticated endpoints:
   - Click "Authorize" button at the top
   - Enter: `Token YOUR_TOKEN_HERE`
   - Click "Authorize"
4. Fill in the parameters
5. Click "Execute"

---

## Common HTTP Status Codes

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `204 No Content` - Request succeeded, no content to return
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Authenticated but not allowed
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server error

---

## Quick Testing Script

Save this as `test_api.sh`:

```bash
#!/bin/bash

# Set your service URL
API_URL="https://YOUR_SERVICE_NAME.onrender.com"

echo "1. Testing health check..."
curl -s "$API_URL/api/health/" | python -m json.tool
echo ""

echo "2. Registering a user..."
RESPONSE=$(curl -s -X POST "$API_URL/api/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }')
echo "$RESPONSE" | python -m json.tool
echo ""

# Extract token from response
TOKEN=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)

if [ -n "$TOKEN" ]; then
  echo "3. Token obtained: $TOKEN"
  echo ""
  
  echo "4. Listing books with authentication..."
  curl -s "$API_URL/api/books/" \
    -H "Authorization: Token $TOKEN" | python -m json.tool | head -30
  echo ""
else
  echo "Failed to get token. User might already exist."
fi
```

Make it executable:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## Error Handling Examples

**Invalid Token:**
```json
{
  "detail": "Invalid token."
}
```

**Missing Required Field:**
```json
{
  "error": "Username, email, and password are required"
}
```

**Duplicate Username:**
```json
{
  "error": "Username already exists"
}
```

**Weak Password:**
```json
{
  "error": "Password must be at least 8 characters long"
}
```

---

## Rate Limiting

The API has rate limiting enabled:
- **Anonymous users**: 100 requests per day
- **Authenticated users**: 1000 requests per day

If you exceed the limit, you'll receive:
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

---

## Support

For issues or questions:
- Check the full API documentation at `/api/docs/`
- Review the deployment guide in `RENDER_DEPLOYMENT_GUIDE.md`
- Check application logs in Render dashboard

Happy testing! 🚀
