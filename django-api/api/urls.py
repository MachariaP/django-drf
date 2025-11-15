from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, CategoryViewSet, PublisherViewSet,
    BookViewSet, ReviewViewSet, health_check, register_user,
    login_user, logout_user, change_password, user_profile,
    api_dashboard
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'publishers', PublisherViewSet, basename='publisher')
router.register(r'books', BookViewSet, basename='book')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', api_dashboard, name='api_dashboard'),
    path('health/', health_check, name='health_check'),
    
    # Authentication endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/change-password/', change_password, name='change_password'),
    path('auth/profile/', user_profile, name='user_profile'),
    
    # Include router URLs (without the root)
    path('', include(router.urls)),
]
