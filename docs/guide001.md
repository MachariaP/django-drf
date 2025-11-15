# 📘 Advanced Django REST Framework Guide - Part 2

> Building on the foundation: Taking your API to production scale with webhooks, real-time features, third-party integrations, and microservices architecture.

---

## 📑 Table of Contents

1. [Introduction](#1-introduction)
2. [Expanding the API - Shopping Cart & Wishlist](#2-expanding-the-api---shopping-cart--wishlist)
3. [Implementing Webhooks](#3-implementing-webhooks)
4. [Real-time Features with Django Channels](#4-real-time-features-with-django-channels)
5. [Third-party Service Integrations](#5-third-party-service-integrations)
6. [Mobile App Integration](#6-mobile-app-integration)
7. [Microservices Architecture](#7-microservices-architecture)
8. [GraphQL Implementation](#8-graphql-implementation)
9. [Advanced Security Features](#9-advanced-security-features)
10. [Monitoring and Logging](#10-monitoring-and-logging)
11. [Performance Optimization](#11-performance-optimization)
12. [API Versioning Strategies](#12-api-versioning-strategies)

---

## 1. Introduction

This guide continues from where the basic guide left off. You should have a working Django REST Framework API with:

✅ Models, Serializers, and ViewSets  
✅ Authentication and Permissions  
✅ Filtering, Pagination, and Documentation  
✅ Basic Testing and Deployment knowledge  

Now we'll expand into production-ready features that make your API:
- **Scalable** - Handle millions of requests efficiently
- **Secure** - Enterprise-level security practices
- **Robust** - Error handling and fault tolerance
- **Integrated** - Connect with external services seamlessly

---

## 2. Expanding the API - Shopping Cart & Wishlist

### 2.1 E-commerce Models

Add these models to `books/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class ShoppingCart(models.Model):
    """Shopping cart for users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.book.price * item.quantity for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Items in shopping cart."""
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'book']


class WishList(models.Model):
    """User wishlist."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)


class WishListItem(models.Model):
    """Items in wishlist."""
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['wishlist', 'book']


class Order(models.Model):
    """Customer orders."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    """Items in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('Book', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
```

### 2.2 Cart & Wishlist ViewSets

Create `books/views_ecommerce.py`:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ShoppingCartViewSet(viewsets.ViewSet):
    """Shopping cart management."""
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get user's cart."""
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart."""
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)
        
        item, created = CartItem.objects.get_or_create(
            cart=cart, book_id=book_id, defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        
        return Response(ShoppingCartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        """Remove item from cart."""
        cart = ShoppingCart.objects.get(user=request.user)
        book_id = request.data.get('book_id')
        CartItem.objects.filter(cart=cart, book_id=book_id).delete()
        return Response(ShoppingCartSerializer(cart).data)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Order management."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        """Create order from cart."""
        cart = ShoppingCart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            shipping_address=request.data.get('shipping_address', '')
        )
        
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                price=cart_item.book.price
            )
        
        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
```

---


### 🧪 Testing Shopping Cart & E-commerce Features - Hands-On

Let's test the shopping cart functionality to ensure everything works perfectly! This is where we make learning fun by actually using what we built.

#### Understanding E-commerce Model Relationships

Before testing, let's understand how these models connect:

```
User ─────┬─── ShoppingCart ───┬─── CartItem ──→ Book
          │                     └─── CartItem ──→ Book
          │
          └─── WishList ──────┬─── WishListItem ──→ Book
          │                   └─── WishListItem ──→ Book
          │
          └─── Order ─────────┬─── OrderItem ──→ Book
                              └─── OrderItem ──→ Book
```

**Key Insights:**
- **OneToOne**: Each user has ONE cart and ONE wishlist
- **ForeignKey**: Each cart item belongs to ONE cart
- **ManyToMany (through models)**: A cart can have many books, a book can be in many carts

#### Step 1: Open Django Shell and Set Up Test Data

```bash
python manage.py shell
```

```python
from books.models import Book, Author, Category, Publisher, ShoppingCart, CartItem, WishList, WishListItem, Order, OrderItem
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

# Create a test user
user = User.objects.create_user(
    username='testcustomer',
    email='customer@example.com',
    password='testpass123'
)
print(f"✅ Created user: {user.username}")

# Create some books for testing (if they don't exist)
author = Author.objects.first()
if not author:
    author = Author.objects.create(
        first_name="Test",
        last_name="Author",
        email="author@example.com"
    )

category = Category.objects.first()
if not category:
    category = Category.objects.create(
        name="Test Category",
        slug="test-category"
    )

# Create test books
books_data = [
    {"title": "Python Basics", "isbn": "1111111111111", "price": Decimal("29.99"), "pages": 300},
    {"title": "Django for Beginners", "isbn": "2222222222222", "price": Decimal("34.99"), "pages": 450},
    {"title": "REST APIs", "isbn": "3333333333333", "price": Decimal("39.99"), "pages": 380},
]

books = []
for data in books_data:
    book, created = Book.objects.get_or_create(
        isbn=data["isbn"],
        defaults={
            'title': data["title"],
            'author': author,
            'price': data["price"],
            'pages': data["pages"],
            'publication_date': date.today(),
            'status': 'available'
        }
    )
    book.categories.add(category)
    books.append(book)
    print(f"{'✅ Created' if created else 'ℹ️  Found'} book: {book.title} (${book.price})")

print(f"\n📚 Total books available: {Book.objects.count()}")
```

#### Step 2: Test Shopping Cart Creation

```python
print("\n🛒 Testing Shopping Cart...")

# The cart is created automatically when first accessed
cart, created = ShoppingCart.objects.get_or_create(user=user)
print(f"{'✅ Created' if created else 'ℹ️  Found'} cart for {user.username}")
print(f"   Cart ID: {cart.id}")
print(f"   Created at: {cart.created_at}")
print(f"   Total items: {cart.items.count()}")

# Check the @property methods
print(f"   Total price: ${cart.total_price}")
print(f"   Total item count: {cart.total_items}")
```

**What We're Learning:**

| Concept | Code | Explanation |
|---------|------|-------------|
| **get_or_create()** | `ShoppingCart.objects.get_or_create(user=user)` | Gets existing cart OR creates new one (atomic operation) |
| **@property** | `cart.total_price` | Calculated field, not stored in database |
| **Lazy evaluation** | `cart.items.all()` | Query not executed until needed |

#### Step 3: Add Items to Cart

```python
print("\n➕ Adding items to cart...")

# Add first book
book1 = books[0]
item1 = CartItem.objects.create(
    cart=cart,
    book=book1,
    quantity=2  # Buying 2 copies
)
print(f"✅ Added {item1.quantity}x '{book1.title}' to cart")

# Add second book
book2 = books[1]
item2 = CartItem.objects.create(
    cart=cart,
    book=book2,
    quantity=1
)
print(f"✅ Added {item2.quantity}x '{book2.title}' to cart")

# Try to add duplicate (should fail due to unique_together constraint)
print("\n🧪 Testing duplicate prevention...")
try:
    duplicate = CartItem.objects.create(
        cart=cart,
        book=book1  # Same book again!
    )
    print("❌ Duplicate creation succeeded (shouldn't happen!)")
except Exception as e:
    print(f"✅ Duplicate prevented: {type(e).__name__}")
    print(f"   This is correct! unique_together=['cart', 'book'] is working")

# Check cart status
cart.refresh_from_db()  # Refresh to get latest data
print(f"\n📊 Cart Status:")
print(f"   Total items: {cart.total_items}")
print(f"   Unique books: {cart.items.count()}")
print(f"   Total price: ${cart.total_price}")

# Detailed breakdown
print(f"\n🛍️ Cart Contents:")
for item in cart.items.select_related('book'):  # Optimization!
    subtotal = item.book.price * item.quantity
    print(f"   - {item.quantity}x {item.book.title}: ${item.book.price} each = ${subtotal}")
```

**Understanding Unique Together:**

```python
# In our model:
class CartItem(models.Model):
    # ...
    class Meta:
        unique_together = ['cart', 'book']

# This means:
# ✅ User A can have Book X in their cart
# ✅ User B can have Book X in their cart
# ❌ User A CANNOT have Book X twice in same cart (database prevents this)

# Why? Prevents duplicate entries. Instead, update quantity:
item = CartItem.objects.get(cart=cart, book=book)
item.quantity += 1  # Increase quantity instead of adding new entry
item.save()
```

#### Step 4: Test Cart Updates (Realistic Scenario)

```python
print("\n🔄 Testing cart updates (like a real e-commerce site)...")

# Scenario: User wants to increase quantity
item = cart.items.first()
old_quantity = item.quantity
item.quantity += 1
item.save()
print(f"✅ Updated {item.book.title}: {old_quantity} → {item.quantity}")
print(f"   New cart total: ${cart.total_price}")

# Scenario: User removes an item
removed_item = cart.items.last()
removed_title = removed_item.book.title
removed_item.delete()
print(f"✅ Removed '{removed_title}' from cart")
print(f"   Remaining items: {cart.items.count()}")
print(f"   New cart total: ${cart.total_price}")

# Scenario: Clear entire cart
print("\n🗑️ Clearing cart...")
deleted_count = cart.items.all().delete()[0]  # Returns (count, {model: count})
print(f"✅ Removed {deleted_count} items")
print(f"   Cart total: ${cart.total_price} (should be 0)")
```

#### Step 5: Test Wishlist Functionality

```python
print("\n⭐ Testing Wishlist...")

# Create wishlist (similar to cart)
wishlist, created = WishList.objects.get_or_create(user=user)
print(f"{'✅ Created' if created else 'ℹ️  Found'} wishlist for {user.username}")

# Add items to wishlist
wishlist_items = []
for book in books[:2]:  # Add first 2 books
    item = WishListItem.objects.create(
        wishlist=wishlist,
        book=book,
        notes=f"Want to read {book.title} someday!"
    )
    wishlist_items.append(item)
    print(f"✅ Added '{book.title}' to wishlist")
    print(f"   Note: {item.notes}")

# View wishlist
print(f"\n💝 Wishlist Contents ({wishlist.items.count()} items):")
for item in wishlist.items.select_related('book'):
    print(f"   - {item.book.title} (${item.book.price})")
    if item.notes:
        print(f"     📝 {item.notes}")
    print(f"     Added: {item.added_at.strftime('%Y-%m-%d %H:%M')}")

# Move from wishlist to cart
print("\n🔄 Moving item from wishlist to cart...")
wishlist_item = wishlist.items.first()
book_to_move = wishlist_item.book

# Add to cart
cart_item = CartItem.objects.create(
    cart=cart,
    book=book_to_move,
    quantity=1
)
print(f"✅ Added '{book_to_move.title}' to cart")

# Remove from wishlist
wishlist_item.delete()
print(f"✅ Removed '{book_to_move.title}' from wishlist")

print(f"\n📊 Summary:")
print(f"   Cart: {cart.items.count()} items")
print(f"   Wishlist: {wishlist.items.count()} items")
```

#### Step 6: Test Order Creation

```python
print("\n📦 Testing Order Creation...")

# First, add items back to cart
for book in books:
    CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': 1}
    )

cart_total = cart.total_price
print(f"Cart ready: {cart.items.count()} items, total: ${cart_total}")

# Create order from cart
order = Order.objects.create(
    user=user,
    total_amount=cart_total,
    shipping_address="123 Main St, City, Country, 12345"
)
print(f"\n✅ Created order #{order.id}")
print(f"   Status: {order.get_status_display()}")
print(f"   Total: ${order.total_amount}")

# Transfer cart items to order items
for cart_item in cart.items.all():
    order_item = OrderItem.objects.create(
        order=order,
        book=cart_item.book,
        quantity=cart_item.quantity,
        price=cart_item.book.price  # Lock in price at time of order!
    )
    print(f"   Added to order: {order_item.quantity}x {order_item.book.title} @ ${order_item.price}")

# Clear cart after order
cart.items.all().delete()
print(f"\n✅ Cart cleared after order")
print(f"   Cart items: {cart.items.count()}")
print(f"   Order items: {order.items.count()}")
```

**Understanding Price Locking:**

```python
# Why do we copy the price to OrderItem?

# Cart Item:
cart_item.book.price  # ← This can change!

# Order Item:
order_item.price  # ← This is LOCKED when order is created

# Example:
# 1. Customer adds book to cart: $29.99
# 2. Customer creates order: Price locked at $29.99
# 3. Admin changes book price: $19.99
# 4. Customer's order still shows: $29.99 (correct!)
# 5. New customers see: $19.99 (current price)

# This protects both customer and business!
```

#### Step 7: Test Order Status Workflow

```python
print("\n🔄 Testing Order Status Workflow...")

# Define status progression
status_flow = ['pending', 'processing', 'shipped', 'delivered']

for status in status_flow:
    order.status = status
    order.save()
    print(f"✅ Order #{order.id} status: {order.get_status_display()}")
    print(f"   Updated at: {order.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
# Try to access order items after delivery
print(f"\n📦 Final Order Summary:")
print(f"   Order ID: {order.id}")
print(f"   Customer: {order.user.username}")
print(f"   Status: {order.get_status_display()}")
print(f"   Items: {order.items.count()}")
print(f"   Total: ${order.total_amount}")
print(f"   Shipping: {order.shipping_address}")

# Calculate order item subtotals
print(f"\n🧾 Itemized Receipt:")
for item in order.items.select_related('book'):
    subtotal = item.price * item.quantity
    print(f"   {item.quantity}x {item.book.title}")
    print(f"      ${item.price} x {item.quantity} = ${subtotal}")

# Verify total
calculated_total = sum(item.price * item.quantity for item in order.items.all())
print(f"\n   Subtotal: ${calculated_total}")
print(f"   Order Total: ${order.total_amount}")
print(f"   ✅ Totals match!" if calculated_total == order.total_amount else "❌ Totals don't match!")
```

#### Step 8: Test Data Integrity and Edge Cases

```python
print("\n🧪 Testing Edge Cases and Data Integrity...")

# Test 1: Can't delete a book that's in an order
test_book = order.items.first().book
print(f"\n1️⃣ Testing cascade protection...")
print(f"   Trying to delete '{test_book.title}' which is in order #{order.id}...")

try:
    test_book.delete()
    print("   ❌ Book deleted (shouldn't happen!)")
except Exception as e:
    print(f"   ✅ Deletion prevented: {type(e).__name__}")
    print(f"   on_delete=models.PROTECT is working!")

# Test 2: Deleting cart clears items
print(f"\n2️⃣ Testing cascade delete...")
test_user = User.objects.create_user(username='testuser2', password='pass')
test_cart = ShoppingCart.objects.create(user=test_user)
test_item = CartItem.objects.create(cart=test_cart, book=books[0], quantity=1)
print(f"   Created test cart with {test_cart.items.count()} item")

item_count_before = CartItem.objects.count()
test_cart.delete()
item_count_after = CartItem.objects.count()
print(f"   Cart deleted")
print(f"   CartItems before: {item_count_before}, after: {item_count_after}")
print(f"   ✅ Cascade delete working! (on_delete=models.CASCADE)")

# Test 3: User can have multiple orders
print(f"\n3️⃣ Testing multiple orders per user...")
orders_count = Order.objects.filter(user=user).count()
print(f"   User '{user.username}' has {orders_count} order(s)")

# Create another order
new_order = Order.objects.create(
    user=user,
    total_amount=Decimal("99.99"),
    shipping_address="456 Oak Ave, Town, Country"
)
print(f"   ✅ Created order #{new_order.id}")
print(f"   User now has {Order.objects.filter(user=user).count()} orders")

# Test 4: Query user's order history
print(f"\n4️⃣ Querying order history...")
user_orders = Order.objects.filter(user=user).order_by('-created_at')
print(f"   📜 {user.username}'s orders (newest first):")
for order in user_orders:
    print(f"      Order #{order.id}: {order.status} - ${order.total_amount}")
    print(f"        Created: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
```

#### 🎯 E-commerce Practice Challenges

**Challenge 1: Complete Shopping Flow**
```python
# Simulate a complete customer journey
print("\n🎯 Challenge 1: Complete Shopping Flow")

# Step 1: Browse and add to cart
new_user = User.objects.create_user(username='shopper', password='pass')
new_cart, _ = ShoppingCart.objects.get_or_create(user=new_user)

# Add 3 different books
for book in Book.objects.all()[:3]:
    CartItem.objects.create(cart=new_cart, book=book, quantity=1)

print(f"✅ Step 1: Added {new_cart.items.count()} books to cart")

# Step 2: Update quantities
for item in new_cart.items.all():
    item.quantity = 2
    item.save()
print(f"✅ Step 2: Updated quantities (total items: {new_cart.total_items})")

# Step 3: Create order
new_order = Order.objects.create(
    user=new_user,
    total_amount=new_cart.total_price,
    shipping_address="Test Address"
)
for cart_item in new_cart.items.all():
    OrderItem.objects.create(
        order=new_order,
        book=cart_item.book,
        quantity=cart_item.quantity,
        price=cart_item.book.price
    )
print(f"✅ Step 3: Created order #{new_order.id} (${new_order.total_amount})")

# Step 4: Clear cart
new_cart.items.all().delete()
print(f"✅ Step 4: Cleared cart")

# Step 5: Verify
print(f"📊 Final State:")
print(f"   Cart items: {new_cart.items.count()}")
print(f"   Order items: {new_order.items.count()}")
print(f"   Order total: ${new_order.total_amount}")
```

**Challenge 2: Calculate Statistics**
```python
# Calculate business metrics
print("\n🎯 Challenge 2: Business Metrics")

from django.db.models import Sum, Count, Avg

# Total revenue
total_revenue = Order.objects.aggregate(
    total=Sum('total_amount')
)['total']
print(f"💰 Total Revenue: ${total_revenue}")

# Orders by status
status_breakdown = Order.objects.values('status').annotate(
    count=Count('id')
).order_by('-count')
print(f"\n📊 Orders by Status:")
for stat in status_breakdown:
    print(f"   {stat['status']}: {stat['count']} orders")

# Average order value
avg_order = Order.objects.aggregate(
    avg=Avg('total_amount')
)['avg']
print(f"\n📈 Average Order Value: ${avg_order:.2f}")

# Most purchased books
top_books = OrderItem.objects.values(
    'book__title'
).annotate(
    total_sold=Sum('quantity')
).order_by('-total_sold')[:5]
print(f"\n📚 Top 5 Best Sellers:")
for i, book in enumerate(top_books, 1):
    print(f"   {i}. {book['book__title']}: {book['total_sold']} sold")
```

**Challenge 3: Abandoned Cart Analysis**
```python
# Find carts that haven't been converted to orders
print("\n🎯 Challenge 3: Abandoned Cart Analysis")

from django.utils import timezone
from datetime import timedelta

# Get carts with items but no recent orders
threshold = timezone.now() - timedelta(days=7)

abandoned_carts = ShoppingCart.objects.filter(
    items__isnull=False  # Has items
).exclude(
    user__orders__created_at__gte=threshold  # But no recent orders
).distinct().annotate(
    item_count=Count('items'),
    cart_value=Sum('items__book__price')
)

print(f"🛒 Abandoned Carts (older than 7 days):")
for cart in abandoned_carts:
    print(f"   User: {cart.user.username}")
    print(f"   Items: {cart.item_count}")
    print(f"   Value: ${cart.cart_value}")
    print(f"   Last updated: {cart.updated_at.strftime('%Y-%m-%d')}")
```

#### 🎓 What You've Learned

✅ **OneToOne Relationships**: Each user has one cart, one wishlist  
✅ **unique_together**: Prevents duplicate cart items  
✅ **@property methods**: Calculated fields (total_price, total_items)  
✅ **on_delete Behavior**: CASCADE vs PROTECT  
✅ **Price Locking**: Why OrderItem stores price separately  
✅ **Order Workflow**: Status progression through lifecycle  
✅ **Data Integrity**: Testing edge cases and constraints  
✅ **Business Metrics**: Aggregations for insights  
✅ **User Journey**: Complete shopping flow simulation  

#### 💡 Pro Tips

1. **Always use get_or_create() for carts**: Prevents duplicate cart creation
   ```python
   cart, created = ShoppingCart.objects.get_or_create(user=request.user)
   ```

2. **Lock prices in orders**: Never reference book.price in order calculations
   ```python
   # ✅ Good: Price locked at order time
   OrderItem.objects.create(..., price=book.price)
   
   # ❌ Bad: Price can change
   order_item.book.price  # Current price, not order price!
   ```

3. **Use select_related for performance**: Avoid N+1 queries
   ```python
   # ✅ Good: 2 queries total
   cart.items.select_related('book')
   
   # ❌ Bad: N+1 queries
   cart.items.all()  # Then accessing item.book each time
   ```

4. **Test data integrity**: Verify cascade behaviors work correctly

5. **Clear cart after order**: Prevents confusion and duplicate orders

**🎮 Make It Fun:** Build a complete e-commerce checkout flow! Add discount codes, tax calculation, shipping options. The more complex the scenario, the more you learn about Django's power!

---

## 3. Implementing Webhooks

Webhooks enable your API to notify external systems when events occur.

### 3.1 Webhook Models

Create `books/models_webhooks.py`:

```python
import uuid
from django.db import models


class WebhookEndpoint(models.Model):
    """Webhook endpoint registration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    url = models.URLField()
    secret = models.CharField(max_length=255)  # For HMAC verification
    events = models.JSONField(default=list)  # Events to subscribe to
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WebhookDelivery(models.Model):
    """Webhook delivery tracking."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    endpoint = models.ForeignKey(WebhookEndpoint, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_status = models.IntegerField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 3.2 Webhook Service

Create `books/services/webhooks.py`:

```python
import hmac
import hashlib
import json
import requests
from django.utils import timezone


class WebhookService:
    """Webhook delivery service."""
    
    @classmethod
    def trigger_event(cls, event_type, payload):
        """Trigger webhook for an event."""
        endpoints = WebhookEndpoint.objects.filter(
            is_active=True,
            events__contains=[event_type]
        )
        
        for endpoint in endpoints:
            cls.send_webhook(endpoint, event_type, payload)
    
    @classmethod
    def send_webhook(cls, endpoint, event_type, payload):
        """Send webhook to endpoint."""
        delivery = WebhookDelivery.objects.create(
            endpoint=endpoint,
            event_type=event_type,
            payload=payload
        )
        
        try:
            webhook_payload = {
                'event_type': event_type,
                'timestamp': timezone.now().isoformat(),
                'data': payload
            }
            
            signature = hmac.new(
                endpoint.secret.encode(),
                json.dumps(webhook_payload).encode(),
                hashlib.sha256
            ).hexdigest()
            
            response = requests.post(
                endpoint.url,
                json=webhook_payload,
                headers={
                    'X-Webhook-Signature': signature,
                    'X-Webhook-Event': event_type
                },
                timeout=30
            )
            
            delivery.response_status = response.status_code
            delivery.status = 'success' if 200 <= response.status_code < 300 else 'failed'
        except Exception as e:
            delivery.status = 'failed'
        
        delivery.attempts += 1
        delivery.save()
```

### 3.3 Webhook Signals

Create `books/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Review
from .services.webhooks import WebhookService


@receiver(post_save, sender=Order)
def order_created_webhook(sender, instance, created, **kwargs):
    """Trigger webhook when order is created."""
    if created:
        WebhookService.trigger_event('order.created', {
            'order_id': instance.id,
            'user_id': instance.user.id,
            'total_amount': str(instance.total_amount),
            'status': instance.status
        })


@receiver(post_save, sender=Review)
def review_posted_webhook(sender, instance, created, **kwargs):
    """Trigger webhook when review is posted."""
    if created:
        WebhookService.trigger_event('review.posted', {
            'review_id': instance.id,
            'book_id': instance.book.id,
            'user_id': instance.user.id,
            'rating': instance.rating
        })
```

---

## 4. Real-time Features with Django Channels

### 4.1 Installation & Setup

```bash
pip install channels channels-redis
```

Update `config/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'channels',
]

ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### 4.2 WebSocket Consumers

Create `books/consumers.py`:

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    """Real-time notifications."""
    
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.group_name = f'user_{self.user.id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def send_notification(self, event):
        """Send notification to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))


class OrderTrackingConsumer(AsyncWebsocketConsumer):
    """Real-time order tracking."""
    
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f'order_{self.order_id}'
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def order_update(self, event):
        """Send order update."""
        await self.send(text_data=json.dumps({
            'type': 'order_update',
            'update': event['update']
        }))
```

### 4.3 WebSocket Routing

Create `books/routing.py`:

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/orders/(?P<order_id>\d+)/$', consumers.OrderTrackingConsumer.as_asgi()),
]
```

Update `config/asgi.py`:

```python
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from books.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
```

### 4.4 Sending Real-time Updates

```python
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Send notification
channel_layer = get_channel_layer()
async_to_sync(channel_layer.group_send)(
    f'user_{user_id}',
    {
        'type': 'send_notification',
        'notification': {
            'title': 'Order Updated',
            'message': 'Your order status has changed'
        }
    }
)
```

---

## 5. Third-party Service Integrations

### 5.1 Payment Processing with Stripe

```bash
pip install stripe
```

Create `books/services/payment.py`:

```python
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    """Stripe payment processing."""
    
    @staticmethod
    def create_payment_intent(amount, currency='usd'):
        """Create a payment intent."""
        return stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            metadata={'integration_check': 'accept_a_payment'}
        )
    
    @staticmethod
    def confirm_payment(payment_intent_id):
        """Confirm a payment."""
        return stripe.PaymentIntent.confirm(payment_intent_id)
    
    @staticmethod
    def create_customer(email, name):
        """Create a Stripe customer."""
        return stripe.Customer.create(email=email, name=name)
```

Add payment endpoint:

```python
from rest_framework.decorators import api_view
from .services.payment import PaymentService

@api_view(['POST'])
def create_payment_intent(request):
    """Create payment intent for order."""
    amount = request.data.get('amount')
    intent = PaymentService.create_payment_intent(amount)
    return Response({'client_secret': intent.client_secret})
```

### 5.2 Email Service with SendGrid

```bash
pip install sendgrid
```

Create `books/services/email.py`:

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


class EmailService:
    """SendGrid email service."""
    
    @staticmethod
    def send_order_confirmation(user, order):
        """Send order confirmation email."""
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=user.email,
            subject=f'Order Confirmation #{order.id}',
            html_content=f'''
                <h1>Thank you for your order!</h1>
                <p>Order ID: {order.id}</p>
                <p>Total: ${order.total_amount}</p>
                <p>Status: {order.get_status_display()}</p>
            '''
        )
        
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    
    @staticmethod
    def send_shipping_notification(user, order):
        """Send shipping notification."""
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=user.email,
            subject=f'Order #{order.id} Shipped!',
            html_content=f'''
                <h1>Your order has been shipped!</h1>
                <p>Order ID: {order.id}</p>
                <p>Track your package at: [Tracking Link]</p>
            '''
        )
        
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        return sg.send(message)
```

### 5.3 Cloud Storage with AWS S3

```bash
pip install django-storages boto3
```

Update `config/settings.py`:

```python
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# Storage backends
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
```

---

## 6. Mobile App Integration

### 6.1 JWT Authentication for Mobile

```bash
pip install djangorestframework-simplejwt
```

Update `config/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
}
```

Add JWT endpoints in `config/urls.py`:

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### 6.2 Push Notifications

```bash
pip install pyfcm
```

Create `books/services/push_notifications.py`:

```python
from pyfcm import FCMNotification
from django.conf import settings


class PushNotificationService:
    """Firebase Cloud Messaging for push notifications."""
    
    def __init__(self):
        self.push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
    
    def send_to_device(self, registration_id, title, message, data=None):
        """Send push notification to a device."""
        return self.push_service.notify_single_device(
            registration_id=registration_id,
            message_title=title,
            message_body=message,
            data_message=data or {}
        )
    
    def send_order_notification(self, user_device_token, order):
        """Send order status notification."""
        return self.send_to_device(
            registration_id=user_device_token,
            title='Order Update',
            message=f'Your order #{order.id} is now {order.get_status_display()}',
            data={'order_id': str(order.id), 'type': 'order_update'}
        )
```

### 6.3 Mobile-Optimized Responses

Create `books/serializers_mobile.py`:

```python
from rest_framework import serializers


class BookMobileSerializer(serializers.ModelSerializer):
    """Optimized serializer for mobile apps."""
    author_name = serializers.CharField(source='author.full_name')
    thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'thumbnail', 'price', 'average_rating']
    
    def get_thumbnail(self, obj):
        """Return optimized thumbnail URL."""
        if obj.cover_image:
            # Return CDN URL or generate thumbnail
            return obj.cover_image.url
        return None
```

---

## 7. Microservices Architecture

### 7.1 Service Decomposition

Break your monolithic API into microservices:

```
┌─────────────────┐
│   API Gateway   │  (Kong, Nginx, or Django)
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼──┐  ┌────▼────┐ ┌──▼──┐
│ Books │ │Users│  │ Orders  │ │ ...  │
│Service│ │Svc  │  │ Service │ │      │
└───────┘ └─────┘  └─────────┘ └─────┘
```

### 7.2 Inter-Service Communication

Create `books/services/inter_service.py`:

```python
import requests
from django.conf import settings


class OrderService:
    """Client for Order microservice."""
    BASE_URL = settings.ORDER_SERVICE_URL
    
    @classmethod
    def create_order(cls, user_id, items, shipping_address):
        """Create order in Order service."""
        response = requests.post(
            f'{cls.BASE_URL}/api/orders/',
            json={
                'user_id': user_id,
                'items': items,
                'shipping_address': shipping_address
            },
            headers={'Authorization': f'Bearer {settings.SERVICE_TOKEN}'}
        )
        response.raise_for_status()
        return response.json()
    
    @classmethod
    def get_order(cls, order_id):
        """Get order from Order service."""
        response = requests.get(
            f'{cls.BASE_URL}/api/orders/{order_id}/',
            headers={'Authorization': f'Bearer {settings.SERVICE_TOKEN}'}
        )
        response.raise_for_status()
        return response.json()


class UserService:
    """Client for User microservice."""
    BASE_URL = settings.USER_SERVICE_URL
    
    @classmethod
    def get_user(cls, user_id):
        """Get user details."""
        response = requests.get(
            f'{cls.BASE_URL}/api/users/{user_id}/',
            headers={'Authorization': f'Bearer {settings.SERVICE_TOKEN}'}
        )
        response.raise_for_status()
        return response.json()
```

### 7.3 Message Queue Integration

```bash
pip install celery redis
```

Create `books/tasks.py`:

```python
from celery import shared_task
from .services.email import EmailService
from .models import Order


@shared_task
def send_order_confirmation_email(order_id):
    """Send order confirmation email asynchronously."""
    order = Order.objects.get(id=order_id)
    EmailService.send_order_confirmation(order.user, order)


@shared_task
def process_order_payment(order_id, payment_method_id):
    """Process order payment asynchronously."""
    from .services.payment import PaymentService
    order = Order.objects.get(id=order_id)
    
    payment = PaymentService.create_payment_intent(order.total_amount)
    # Process payment...
    
    if payment.status == 'succeeded':
        order.status = 'processing'
        order.save()
```

---

## 8. GraphQL Implementation

### 8.1 Installation

```bash
pip install graphene-django
```

Update `config/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'graphene_django',
]

GRAPHENE = {
    'SCHEMA': 'books.schema.schema'
}
```

### 8.2 GraphQL Schema

Create `books/schema.py`:

```python
import graphene
from graphene_django import DjangoObjectType
from .models import Book, Author, Review


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = '__all__'


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = '__all__'


class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int())
    all_authors = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, id=graphene.Int())
    books_by_author = graphene.List(BookType, author_id=graphene.Int())
    
    def resolve_all_books(self, info):
        return Book.objects.select_related('author').all()
    
    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)
    
    def resolve_all_authors(self, info):
        return Author.objects.all()
    
    def resolve_author(self, info, id):
        return Author.objects.get(pk=id)
    
    def resolve_books_by_author(self, info, author_id):
        return Book.objects.filter(author_id=author_id)


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.Int(required=True)
        isbn = graphene.String(required=True)
        price = graphene.Float(required=True)
    
    book = graphene.Field(BookType)
    
    def mutate(self, info, title, author_id, isbn, price):
        book = Book.objects.create(
            title=title,
            author_id=author_id,
            isbn=isbn,
            price=price
        )
        return CreateBook(book=book)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
```

### 8.3 GraphQL Endpoint

Update `config/urls.py`:

```python
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # ...
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
```

### 8.4 GraphQL Queries

```graphql
# Get all books
query {
  allBooks {
    id
    title
    author {
      fullName
    }
    price
  }
}

# Get specific book
query {
  book(id: 1) {
    title
    author {
      firstName
      lastName
    }
    reviews {
      rating
      comment
    }
  }
}

# Create book
mutation {
  createBook(
    title: "New Book"
    authorId: 1
    isbn: "1234567890123"
    price: 29.99
  ) {
    book {
      id
      title
    }
  }
}
```

---

## 9. Advanced Security Features

### 9.1 Rate Limiting per User

Create `books/throttles.py`:

```python
from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
    rate = '60/min'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
    rate = '1000/day'


class PremiumUserRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        if request.user.is_authenticated and request.user.profile.is_premium:
            return True  # No limit for premium users
        return super().allow_request(request, view)
```

### 9.2 API Key Authentication

Create `books/authentication.py`:

```python
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    """API key authentication for service-to-service calls."""
    
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return None
        
        try:
            key = APIKey.objects.get(key=api_key, is_active=True)
            return (key.user, None)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
```

### 9.3 Content Security Policy

Update `config/settings.py`:

```python
MIDDLEWARE = [
    # ...
    'django.middleware.security.SecurityMiddleware',
]

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 9.4 Input Validation & Sanitization

```python
from django.core.validators import URLValidator, EmailValidator
from rest_framework import serializers
import bleach


class SecureBookSerializer(serializers.ModelSerializer):
    """Serializer with security validations."""
    
    def validate_description(self, value):
        """Sanitize HTML in description."""
        allowed_tags = ['p', 'br', 'strong', 'em', 'u']
        return bleach.clean(value, tags=allowed_tags, strip=True)
    
    def validate_isbn(self, value):
        """Validate ISBN format."""
        if not value.isdigit() or len(value) not in [10, 13]:
            raise serializers.ValidationError('Invalid ISBN format')
        return value
```

---

## 10. Monitoring and Logging

### 10.1 Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

### 10.2 Application Performance Monitoring (APM)

```bash
pip install sentry-sdk
```

Update `config/settings.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### 10.3 Custom Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'books': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### 10.4 API Metrics Collection

Create `books/middleware/metrics.py`:

```python
import time
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('books')


class APIMetricsMiddleware(MiddlewareMixin):
    """Collect API metrics."""
    
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(f'{request.method} {request.path} - {response.status_code} - {duration:.2f}s')
        return response
```

---

## 11. Performance Optimization

### 11.1 Database Query Optimization

```python
# Bad: N+1 queries
books = Book.objects.all()
for book in books:
    print(book.author.name)  # Triggers new query each time

# Good: Use select_related
books = Book.objects.select_related('author').all()
for book in books:
    print(book.author.name)  # No additional queries

# Good: Use prefetch_related for many-to-many
books = Book.objects.prefetch_related('categories', 'reviews').all()
```

### 11.2 Caching Strategies

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action


class BookViewSet(viewsets.ModelViewSet):
    
    @cache_page(60 * 15)  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """Get bestsellers with caching."""
        cache_key = 'bestsellers'
        bestsellers = cache.get(cache_key)
        
        if bestsellers is None:
            bestsellers = Book.objects.annotate(
                review_count=Count('reviews')
            ).order_by('-review_count')[:10]
            
            serializer = self.get_serializer(bestsellers, many=True)
            bestsellers = serializer.data
            cache.set(cache_key, bestsellers, 60 * 60)  # Cache for 1 hour
        
        return Response(bestsellers)
```

### 11.3 Database Indexing

```python
class Book(models.Model):
    # ...
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author', 'publication_date']),
            models.Index(fields=['-created_at']),
        ]
```

### 11.4 Asynchronous Task Processing

```python
from celery import shared_task


@shared_task
def generate_book_report(book_id):
    """Generate book sales report asynchronously."""
    book = Book.objects.get(id=book_id)
    # Complex report generation logic
    return report


@shared_task
def bulk_update_prices():
    """Update book prices from external source."""
    # Bulk update logic
    pass
```

---

## 12. API Versioning Strategies

### 12.1 URL Path Versioning

```python
# config/urls.py
urlpatterns = [
    path('api/v1/', include('books.urls_v1')),
    path('api/v2/', include('books.urls_v2')),
]
```

### 12.2 Header Versioning

```python
# config/settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}

# books/views.py
class BookViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return BookSerializerV2
        return BookSerializerV1
```

### 12.3 Deprecation Strategy

```python
class DeprecatedEndpointMixin:
    """Mixin for deprecated endpoints."""
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.headers['Warning'] = (
            '299 - "This endpoint is deprecated and will be removed in v3. '
            'Please use /api/v2/books/ instead."'
        )
```

---

## 🎉 Conclusion

Congratulations! You've learned advanced Django REST Framework features:

✅ **E-commerce Features** - Shopping carts, wishlists, and orders  
✅ **Webhooks** - Event-driven architecture  
✅ **Real-time Communication** - WebSockets with Django Channels  
✅ **Third-party Integrations** - Stripe, SendGrid, AWS S3  
✅ **Mobile Optimization** - JWT auth and push notifications  
✅ **Microservices** - Service decomposition and communication  
✅ **GraphQL** - Flexible query language  
✅ **Security** - Advanced authentication and authorization  
✅ **Monitoring** - Logging, metrics, and APM  
✅ **Performance** - Caching, optimization, and async tasks  
✅ **Versioning** - API evolution strategies  

### Next Steps

1. **Implement CI/CD** - Automate testing and deployment
2. **Add Kubernetes** - Container orchestration
3. **Implement API Gateway** - Kong or AWS API Gateway
4. **Add Machine Learning** - Recommendation engine
5. **Implement Search** - Elasticsearch integration
6. **Add Analytics** - Google Analytics or custom solution

### Best Practices Summary

🔒 **Security First**

Security should be your top priority when building production APIs. Here's why each practice matters:

- **Always use HTTPS in production**
  
  HTTPS encrypts all data transmitted between your API and clients, protecting sensitive information like passwords, authentication tokens, and personal data from being intercepted by malicious actors. Without HTTPS, attackers can perform man-in-the-middle attacks to steal credentials or inject malicious content. In production, configure your web server (nginx, Apache) with SSL/TLS certificates from providers like Let's Encrypt (free) or commercial Certificate Authorities.
  
  ```python
  # In settings.py for production
  SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS
  SECURE_HSTS_SECONDS = 31536000  # Force HTTPS for 1 year
  SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
  CSRF_COOKIE_SECURE = True  # Protect CSRF tokens
  ```

- **Implement rate limiting**
  
  Rate limiting prevents abuse by restricting how many requests a client can make within a time period. This protects your API from:
  - **Denial of Service (DoS) attacks**: Malicious users overwhelming your server
  - **Brute force attacks**: Automated password guessing attempts
  - **Resource exhaustion**: Heavy users consuming disproportionate server resources
  - **Cost management**: Excessive API calls increasing infrastructure costs
  
  DRF provides built-in throttling classes. For example, limit users to 100 requests per hour and 1000 per day to ensure fair usage while maintaining service availability for all users.

- **Validate and sanitize inputs**
  
  Never trust user input. Every piece of data coming from clients could be malicious. Validation ensures data meets your requirements (correct format, type, length), while sanitization removes or escapes potentially harmful content. This prevents:
  - **SQL Injection**: Malicious SQL code in database queries
  - **Cross-Site Scripting (XSS)**: Malicious JavaScript injected into pages
  - **Data corruption**: Invalid data breaking your application logic
  
  Use DRF serializers for validation, Django's ORM for SQL injection prevention, and libraries like `bleach` to sanitize HTML content. Always validate on the server side even if you validate on the client.

- **Use JWT for mobile apps**
  
  JSON Web Tokens (JWT) are perfect for mobile apps because they're stateless and self-contained. Unlike session-based auth that requires server-side storage, JWTs store user information in the token itself, making them:
  - **Scalable**: No server-side session storage needed
  - **Efficient**: Reduce database lookups for authentication
  - **Cross-domain friendly**: Work seamlessly across different domains and services
  - **Mobile-optimized**: Easier to manage on mobile devices with automatic token refresh
  
  Implement with `djangorestframework-simplejwt` and use short-lived access tokens (15-60 minutes) with longer refresh tokens (7-30 days) for security.

- **Keep dependencies updated**
  
  Outdated packages are a major security risk. Vulnerabilities are discovered regularly, and attackers actively exploit known weaknesses in old library versions. Keeping dependencies updated:
  - **Patches security vulnerabilities**: Fixes known exploits before attackers can use them
  - **Improves performance**: Newer versions often include optimizations
  - **Maintains compatibility**: Prevents breaking changes that accumulate over time
  - **Reduces technical debt**: Easier to upgrade incrementally than in large jumps
  
  Use tools like `pip list --outdated`, `safety check` for security scanning, and Dependabot for automated updates. Test updates in staging before production deployment.

⚡ **Performance**

Performance directly impacts user experience and operational costs. Slow APIs frustrate users and waste resources:

- **Use database query optimization**
  
  Database queries are often the biggest performance bottleneck. Poor queries can make your API hundreds of times slower. Key optimization techniques:
  - **N+1 query problem**: When loading related objects in a loop creates one query per item. Use `select_related()` for foreign keys and `prefetch_related()` for many-to-many relationships to load everything in 1-2 queries instead of hundreds.
  - **Only fetch needed data**: Use `.only()` to load specific fields, `.values()` for dictionaries, reducing memory and transfer overhead.
  - **Aggregate in database**: Use `.annotate()` and `.aggregate()` to calculate counts, sums, averages in the database rather than in Python.
  
  Example: Loading 100 books with authors - bad code makes 101 queries (1 for books + 100 for authors), optimized code makes just 2 queries using `select_related('author')`.

- **Implement caching strategies**
  
  Caching stores frequently accessed data in fast memory (Redis, Memcached) so you don't re-compute or re-fetch it repeatedly. This dramatically improves response times and reduces database load:
  - **Query caching**: Cache expensive database queries (e.g., bestseller lists, trending items)
  - **API response caching**: Cache entire API responses for data that doesn't change often
  - **Fragment caching**: Cache parts of responses (e.g., user profiles, product details)
  - **Cache invalidation**: Clear cache when data changes to prevent stale data
  
  A well-cached API can respond in milliseconds instead of seconds. Use Django's cache framework with Redis for best performance. Set appropriate expiration times based on data volatility.

- **Use async tasks for heavy operations**
  
  Long-running operations block your API from handling other requests, creating timeouts and poor user experience. Move heavy tasks to background workers:
  - **Email sending**: Processing and sending emails can take seconds
  - **File processing**: Generating PDFs, resizing images, processing uploads
  - **External API calls**: Third-party services may be slow or unreliable
  - **Batch operations**: Bulk updates, data imports, report generation
  
  Use Celery with Redis/RabbitMQ to queue tasks. Your API responds immediately with a task ID, processes in background, and notifies completion via webhooks or polling. This keeps your API responsive (< 200ms) even for complex operations.

- **Monitor performance metrics**
  
  You can't optimize what you don't measure. Performance monitoring helps you:
  - **Identify bottlenecks**: Discover which endpoints are slow and why
  - **Detect anomalies**: Catch performance degradation before users complain
  - **Track improvements**: Verify that optimizations actually work
  - **Capacity planning**: Predict when you'll need to scale resources
  
  Monitor: response times (p50, p95, p99), throughput (requests/second), error rates, database query times, cache hit rates, and resource usage (CPU, memory). Tools like New Relic, DataDog, or Django Debug Toolbar help identify issues.

- **Optimize database indexes**
  
  Database indexes are like book indexes - they help find data quickly without scanning everything. Without proper indexes, queries get exponentially slower as data grows:
  - **Single-column indexes**: Speed up filtering and sorting on frequently queried fields (e.g., `created_at`, `status`, `user_id`)
  - **Composite indexes**: Optimize queries filtering on multiple fields together
  - **Trade-offs**: Indexes speed up reads but slow down writes (inserts/updates) and use disk space
  
  Index fields used in `WHERE`, `ORDER BY`, `JOIN`, and foreign keys. Use `django-debug-toolbar` to identify slow queries. A query scanning 1 million rows without an index might take seconds; with an index, milliseconds.

📊 **Scalability**

Scalability ensures your API handles growth - more users, more data, more features - without degrading:

- **Design for horizontal scaling**
  
  Horizontal scaling means adding more servers rather than making one server bigger (vertical scaling). This is crucial because:
  - **No single point of failure**: If one server crashes, others continue serving
  - **Cost-effective**: Add cheaper commodity servers instead of expensive powerful ones
  - **Unlimited growth**: Keep adding servers as needed, no upper limit
  - **Geographic distribution**: Deploy servers worldwide for lower latency
  
  Design stateless APIs where any server can handle any request. Use external storage for sessions (Redis), files (S3), and databases (managed services). Avoid storing user data in server memory or local files. This lets you scale from 1 to 1000 servers seamlessly.

- **Use message queues**
  
  Message queues decouple services and enable asynchronous processing, essential for scalability:
  - **Handle traffic spikes**: Queue requests when servers are busy, process when capacity available
  - **Retry failed operations**: Automatically retry failed tasks without losing work
  - **Service decoupling**: Services communicate via messages, not direct calls, allowing independent scaling
  - **Load distribution**: Distribute work across multiple workers automatically
  
  Use RabbitMQ, Redis, or AWS SQS. For example, when thousands of orders arrive simultaneously, queue them for processing rather than overwhelming your servers. Workers process queued items at sustainable pace.

- **Implement microservices when needed**
  
  Microservices split your monolithic API into smaller, independent services. Consider this when:
  - **Different scaling needs**: User service needs 10 servers while order service needs 2
  - **Team organization**: Different teams can work on different services independently
  - **Technology diversity**: Use Python for one service, Node.js for another based on strengths
  - **Fault isolation**: A bug in one service doesn't crash the entire application
  
  Start with a monolith, split when pain points emerge. Over-engineering with microservices too early adds complexity without benefits. Common split: User Service, Product Service, Order Service, Payment Service, each with its own database.

- **Use CDN for static files**
  
  Content Delivery Networks (CDN) distribute your static files (images, CSS, JavaScript, documents) across servers worldwide:
  - **Reduced latency**: Users download from nearby servers (Tokyo user from Tokyo server, not New York)
  - **Bandwidth savings**: CDN serves files, saving your server bandwidth and costs
  - **Improved reliability**: Files remain available even if your main server is down
  - **Better performance**: CDNs optimize file delivery with compression and caching
  
  Use services like CloudFlare, AWS CloudFront, or Fastly. Configure Django to serve static/media files via CDN in production. This is especially critical for global audiences and media-heavy applications.

- **Load balance traffic**
  
  Load balancers distribute incoming requests across multiple servers, preventing any single server from being overwhelmed:
  - **Even distribution**: Spread requests evenly so all servers work at optimal capacity
  - **Health checks**: Automatically remove failing servers from rotation
  - **Zero-downtime deploys**: Route traffic away from servers during updates
  - **SSL termination**: Handle HTTPS encryption/decryption at load balancer, reducing server load
  
  Use nginx, HAProxy, AWS ELB, or Google Cloud Load Balancing. Common algorithms: round-robin (cycle through servers), least connections (route to least busy), IP hash (same user to same server for session stickiness).

🧪 **Quality**

Quality practices ensure your code works correctly, is maintainable, and can evolve safely:

- **Write comprehensive tests**
  
  Tests are your safety net, catching bugs before users do. Comprehensive testing means:
  - **Unit tests**: Test individual functions and methods in isolation (80% of your tests)
  - **Integration tests**: Test how components work together (databases, APIs, services)
  - **End-to-end tests**: Test complete user workflows from start to finish
  - **Edge cases**: Test boundary conditions, invalid inputs, error scenarios
  
  Aim for 80%+ code coverage but focus on critical paths. Test models, serializers, views, permissions, and business logic. Use Django's test framework and pytest. Write tests before fixing bugs (regression tests) to prevent the same bug from returning. Good tests let you refactor confidently.

- **Use code linters**
  
  Linters automatically check code for errors, style violations, and potential bugs before runtime:
  - **Catch errors early**: Find syntax errors, undefined variables, unused imports before they cause runtime failures
  - **Enforce consistency**: Ensure entire team follows same style guidelines (PEP 8 for Python)
  - **Code quality**: Detect code smells, complexity issues, security vulnerabilities
  - **Save review time**: Automate style feedback so code reviews focus on logic and design
  
  Use `flake8` for style checking, `pylint` for code quality, `black` for auto-formatting, `mypy` for type checking. Run in pre-commit hooks and CI pipeline. Consistent code is easier to read, review, and maintain.

- **Implement CI/CD**
  
  Continuous Integration/Continuous Deployment automates testing and deployment, making releases fast and reliable:
  - **Automated testing**: Run all tests on every commit, catching bugs immediately
  - **Consistent builds**: Build in clean environment, eliminating "works on my machine" issues
  - **Fast feedback**: Developers know within minutes if their changes broke something
  - **Safe deployments**: Automated deploy process reduces human error, enables frequent releases
  
  Use GitHub Actions, GitLab CI, or Jenkins. Typical pipeline: code push → run linters → run tests → build → deploy to staging → run integration tests → deploy to production. Deploy multiple times daily instead of monthly, reducing risk and delivering value faster.

- **Monitor errors with Sentry**
  
  Sentry captures and reports errors in production, helping you fix issues before they impact many users:
  - **Real-time alerts**: Get notified immediately when errors occur, with full stack traces
  - **Error grouping**: Automatically groups similar errors so you see patterns, not noise
  - **User context**: See which users are affected, on what browsers/devices, with what data
  - **Release tracking**: Track error rates across deployments to catch regressions
  
  Integrate Sentry to catch exceptions, log context (user, request, environment), and track error frequency. Fix high-frequency errors first. Monitor after deployments for new error patterns. This proactive approach beats waiting for user bug reports.

- **Document your API**
  
  Good documentation is crucial for API adoption and reduces support burden:
  - **API reference**: Auto-generate with DRF's built-in browsable API or tools like Swagger/OpenAPI
  - **Getting started guide**: Help new users make their first successful API call quickly
  - **Authentication guide**: Clear instructions on obtaining and using API credentials
  - **Code examples**: Show common use cases in multiple programming languages (curl, Python, JavaScript)
  - **Error codes**: Document all error responses with explanations and solutions
  
  Use tools like `drf-yasg` or `drf-spectacular` for automatic OpenAPI documentation. Keep docs updated with code changes. Good documentation increases API adoption, reduces support tickets, and improves developer experience.

---

**Happy Coding! 🚀**

*Remember: Building a production-grade API is an iterative process. Start with core features, test thoroughly, and expand gradually. Focus on security, performance, and user experience at every step.*
