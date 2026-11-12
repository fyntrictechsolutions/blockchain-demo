from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, BatchViewSet

# 1. Create a router object
router = DefaultRouter()

# 2. Register our ViewSets with the router
router.register(r'products', ProductViewSet, basename='product')
router.register(r'batches', BatchViewSet, basename='batch')

# 3. The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]