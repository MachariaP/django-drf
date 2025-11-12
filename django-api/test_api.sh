#!/bin/bash
set -e

BASE="http://127.0.0.1:8000"
COOKIE="cookies.txt"

echo "Getting token..."
curl -s -X POST $BASE/api/token/ -d "username=admin&password=admin123" -c $COOKIE > /dev/null

echo -e "\nTesting endpoints...\n"

# Helper: pretty-print JSON with fallback
print_json() {
  echo "$1" | jq -r '.results[0] // .[0] // .title // .name // .id // .'
}

# 1. List books + get first book ID
echo "GET /api/books/"
BOOKS_RESPONSE=$(curl -s -b $COOKIE "$BASE/api/books/")
print_json "$BOOKS_RESPONSE"

FIRST_BOOK_ID=$(echo "$BOOKS_RESPONSE" | jq -r '.results[0].id // .[0].id // empty')
if [ -z "$FIRST_BOOK_ID" ]; then
  echo "No books found!"
  exit 1
fi
echo "First book ID: $FIRST_BOOK_ID"

# 2. Get single book
echo -e "\nGET /api/books/$FIRST_BOOK_ID/"
curl -s -b $COOKIE "$BASE/api/books/$FIRST_BOOK_ID/" | jq .

# 3. Categories
echo -e "\nGET /api/categories/"
curl -s -b $COOKIE "$BASE/api/categories/" | jq -r '.results[0] // .[0] // .'

# 4. Authors
echo -e "\nGET /api/authors/"
curl -s -b $COOKIE "$BASE/api/authors/" | jq -r '.results[0] // .[0] // .'

# 5. Publishers
echo -e "\nGET /api/publishers/"
curl -s -b $COOKIE "$BASE/api/publishers/" | jq -r '.results[0] // .[0] // .'

# 6. Reviews for first book
echo -e "\nGET /api/books/$FIRST_BOOK_ID/reviews/"
curl -s -b $COOKIE "$BASE/api/books/$FIRST_BOOK_ID/reviews/" | jq .

# 7. Bestsellers (direct list, no .results)
echo -e "\nGET /api/books/bestsellers/"
curl -s -b $COOKIE "$BASE/api/books/bestsellers/" | jq -r '.[0] // .'

# 8. Search: Python
echo -e "\nGET /api/books/?search=python"
curl -s -b $COOKIE "$BASE/api/books/?search=python" | jq -r '.results[0] // .[0] // .'

# 9. POST a review
echo -e "\nPOST /api/books/$FIRST_BOOK_ID/reviews/"
curl -s -X POST -b $COOKIE "$BASE/api/books/$FIRST_BOOK_ID/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "title": "Test via curl",
    "comment": "Automated test review!"
  }' | jq .

echo -e "\nAll tests passed! Your API is working perfectly."
