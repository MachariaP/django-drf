from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, CategoryViewSet, PublisherViewSet,
    BookViewSet, ReviewViewSet
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'publishers', PublisherViewSet, basename='publisher')
router.register(r'books', BookViewSet, basename='book')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
