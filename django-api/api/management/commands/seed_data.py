#!/usr/bin/env python
"""
Seed the bookstore DB with >20 programming books.
Run:  python seed_programming_books.py
"""

import os
import random
from datetime import date, timedelta

# ----------------------------------------------------------------------
# 1. Django setup
# ----------------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # <-- change if your settings module is different
import django
django.setup()

from django.contrib.auth.models import User
from api.models import Author, Category, Publisher, Book, Review

# ----------------------------------------------------------------------
# 2. Helper: get-or-create objects
# ----------------------------------------------------------------------
def goc(model, **kwargs):
    """Get or create – returns (obj, created)"""
    obj, created = model.objects.get_or_create(**kwargs)
    if created:
        obj.save()
    return obj

# ----------------------------------------------------------------------
# 3. Create a super-user (optional, for admin / reviews)
# ----------------------------------------------------------------------
admin_user, _ = User.objects.get_or_create(
    username="admin",
    defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True},
)
if not admin_user.has_usable_password():
    admin_user.set_password("admin123")
    admin_user.save()

# ----------------------------------------------------------------------
# 4. Categories (programming-related)
# ----------------------------------------------------------------------
prog_cats = [
    ("Python", "python", "Python programming language"),
    ("JavaScript", "javascript", "Web development with JS"),
    ("Java", "java", "Enterprise Java"),
    ("C++", "cpp", "Systems programming with C++"),
    ("Go", "go", "Go programming language"),
    ("Rust", "rust", "Systems programming with Rust"),
    ("Data Science", "data-science", "Data analysis & ML"),
    ("Web Development", "web-dev", "HTML/CSS/JS + frameworks"),
    ("DevOps", "devops", "CI/CD, containers, cloud"),
    ("Algorithms", "algorithms", "Data structures & algorithms"),
]

for name, slug, desc in prog_cats:
    goc(Category, name=name, defaults={"slug": slug, "description": desc})

# ----------------------------------------------------------------------
# 5. Publishers
# ----------------------------------------------------------------------
publishers = [
    ("O'Reilly Media", "Sebastopol", "USA", "https://www.oreilly.com"),
    ("Manning Publications", "Shelter Island", "USA", "https://www.manning.com"),
    ("Pragmatic Bookshelf", "Raleigh", "USA", "https://pragprog.com"),
    ("Packt Publishing", "Birmingham", "UK", "https://www.packtpub.com"),
    ("No Starch Press", "San Francisco", "USA", "https://nostarch.com"),
    ("Addison-Wesley", "Boston", "USA", "https://www.pearson.com"),
]

for name, city, country, web in publishers:
    goc(Publisher, name=name, defaults={"city": city, "country": country, "website": web})

# ----------------------------------------------------------------------
# 6. Programming books data (title, author, isbn, pub_date, pages, price)
# ----------------------------------------------------------------------
book_data = [
    # Python
    ("Fluent Python", "Luciano Ramalho", "9781491946008", date(2015, 3, 15), 792, 49.99),
    ("Python Crash Course", "Eric Matthes", "9781593279285", date(2019, 5, 1), 544, 29.99),
    ("Automate the Boring Stuff with Python", "Al Sweigart", "9781593275993", date(2015, 4, 14), 504, 24.99),
    ("Effective Python", "Brett Slatkin", "9780134034287", date(2015, 3, 10), 256, 39.99),
    ("Python Cookbook", "David Beazley", "9781449340377", date(2013, 5, 10), 706, 54.99),

    # JavaScript
    ("Eloquent JavaScript", "Marijn Haverbeke", "9781593279509", date(2018, 12, 4), 472, 29.99),
    ("You Don't Know JS: Scope & Closures", "Kyle Simpson", "9781449335581", date(2014, 3, 28), 98, 19.99),
    ("JavaScript: The Good Parts", "Douglas Crockford", "9780596517748", date(2008, 5, 1), 176, 24.99),
    ("Learning React", "Alex Banks & Eve Porcello", "9781492051724", date(2020, 6, 9), 350, 39.99),

    # Java
    ("Effective Java", "Joshua Bloch", "9780134685991", date(2017, 12, 27), 412, 44.99),
    ("Java: The Complete Reference", "Herbert Schildt", "9781260440232", date(2019, 2, 1), 1248, 59.99),

    # C++
    ("C++ Primer", "Stanley B. Lippman", "9780321714111", date(2012, 8, 6), 976, 64.99),
    ("Accelerated C++", "Andrew Koenig", "9780201703535", date(2000, 8, 25), 352, 39.99),

    # Go
    ("The Go Programming Language", "Alan A. A. Donovan", "9780134190441", date(2015, 10, 26), 400, 44.99),
    ("Go Programming Language", "John P. Baugh", "9780134190560", date(2016, 3, 15), 380, 39.99),

    # Rust
    ("The Rust Programming Language", "Steve Klabnik", "9781593278284", date(2019, 6, 12), 560, 34.99),
    ("Programming Rust", "Jim Blandy", "9781491927284", date(2021, 2, 9), 738, 49.99),

    # Data Science / ML
    ("Hands-On Machine Learning with Scikit-Learn", "Aurélien Géron", "9781492032649", date(2019, 8, 15), 856, 59.99),
    ("Python for Data Analysis", "Wes McKinney", "9781491957660", date(2017, 10, 1), 550, 44.99),

    # Web / DevOps
    ("Clean Code", "Robert C. Martin", "9780132350884", date(2008, 8, 1), 464, 44.99),
    ("The DevOps Handbook", "Gene Kim", "9781942788003", date(2016, 10, 1), 480, 34.99),
    ("Site Reliability Engineering", "Betsy Beyer", "9781491929127", date(2016, 4, 15), 552, 49.99),

    # Algorithms
    ("Introduction to Algorithms", "Thomas H. Cormen", "9780262033848", date(2009, 7, 31), 1312, 99.99),
    ("Grokking Algorithms", "Aditya Bhargava", "9781617292231", date(2016, 5, 15), 256, 29.99),
]

# ----------------------------------------------------------------------
# 7. Create authors, publishers, books
# ----------------------------------------------------------------------
created_books = []

for title, author_name, isbn, pub_date, pages, price in book_data:
    # ---- author ----
    first, *rest = author_name.split()
    last = rest[-1] if rest else ""
    author, _ = Author.objects.get_or_create(
        first_name=first,
        last_name=last,
        defaults={"email": f"{first.lower()}.{last.lower()}@example.com".replace(" ", ""),
                  "birth_date": date(1970, 1, 1)}   # dummy
    )

    # ---- publisher (random) ----
    publisher = random.choice(Publisher.objects.all())

    # ---- categories (match title keywords) ----
    cat_names = []
    lower = title.lower()
    if any(k in lower for k in ["python", "django", "flask"]): cat_names.append("Python")
    if any(k in lower for k in ["javascript", "react", "node"]): cat_names.append("JavaScript")
    if "java" in lower: cat_names.append("Java")
    if "c++" in lower: cat_names.append("C++")
    if "go" in lower: cat_names.append("Go")
    if "rust" in lower: cat_names.append("Rust")
    if any(k in lower for k in ["machine learning", "data", "ml"]): cat_names.append("Data Science")
    if any(k in lower for k in ["web", "html", "css"]): cat_names.append("Web Development")
    if any(k in lower for k in ["devops", "docker", "kubernetes"]): cat_names.append("DevOps")
    if any(k in lower for k in ["algorithm", "data structure"]): cat_names.append("Algorithms")
    # fallback
    if not cat_names:
        cat_names = ["Web Development"]

    categories = Category.objects.filter(name__in=cat_names)

    # ---- create book (idempotent by ISBN) ----
    book, created = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            "title": title,
            "author": author,
            "publisher": publisher,
            "publication_date": pub_date,
            "pages": pages,
            "price": price,
            "description": f"Practical guide to {title.split(':')[0]}.",
            "status": random.choice(["available", "available", "out_of_stock"]),
        },
    )
    if created:
        book.categories.set(categories)
        created_books.append(book)

print(f"Created {len(created_books)} new programming books.")

# ----------------------------------------------------------------------
# 8. Add a few random reviews (1-3 per book) — SAFE VERSION
# ----------------------------------------------------------------------
print("Adding reviews...")

# Ensure we have at least 3 users
users = list(User.objects.all())
if len(users) < 3:
    for i in range(3 - len(users)):
        User.objects.create_user(
            username=f"user{i+1}",
            email=f"user{i+1}@example.com",
            password="user123"
        )
    users = list(User.objects.all())

review_titles = [
    "Excellent resource!", "Clear explanations", "A must-read for beginners",
    "Helped me land a job", "Too verbose", "Great examples", "Outdated",
    "Perfect reference", "Loved the exercises", "Worth every penny"
]
review_comments = [
    "The code samples are spot-on and easy to follow.",
    "I finally understood closures thanks to this book.",
    "A bit dense but packed with knowledge.",
    "Highly recommended for interview prep.",
    "Examples are in Python 2 – needs an update.",
    "Best book I've read on the topic.",
    "Wish it had more diagrams.",
]

created_reviews = 0
for book in created_books:
    num_reviews = random.randint(1, 3)
    available_users = users.copy()
    random.shuffle(available_users)

    for _ in range(num_reviews):
        if not available_users:
            break  # no more users

        user = available_users.pop()  # use a different user

        # Skip if this user already reviewed this book
        if Review.objects.filter(book=book, user=user).exists():
            continue

        Review.objects.create(
            book=book,
            user=user,
            rating=random.randint(3, 5),
            title=random.choice(review_titles),
            comment=random.choice(review_comments),
        )
        created_reviews += 1

print(f"Added {created_reviews} unique reviews.")
print("\nSeeding complete! Visit http://127.0.0.1:8000/api/books/ to explore.")

