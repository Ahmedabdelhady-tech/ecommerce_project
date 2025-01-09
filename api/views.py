from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from products.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, CustomTokenObtainPairSerializer
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache

class ProductPagination(PageNumberPagination):
    page_size = 10  # Increased the default page size
    page_size_query_param = 'page_size'
    max_page_size = 50  # Increased the maximum page size limit

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """
        List all categories with optional filters.
        """
        return super().list(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('price')  # Default ordering by price
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    # Filters for searching and ordering
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'category__name']
    ordering_fields = ['price', 'created_date']
    pagination_class = ProductPagination

    def get_permissions(self):
        """
        Customize permissions to allow only authenticated users to perform certain actions.
        """
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAuthenticated]  # Only authenticated users can manage products
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Non-authenticated users can only view products
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Handle product creation with error handling.
        """
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An error occurred during product creation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Handle product updates with error handling.
        """
        try:
            return super().update(request, *args, **kwargs)
        except NotFound:
            return Response({"detail": f"Product with ID {kwargs['pk']} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"An error occurred during product update: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        Handle product deletion with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except NotFound:
            return Response({"detail": f"Product with ID {kwargs['pk']} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"An error occurred during product deletion: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        """
        List all products with optional filters and cache the result.
        """
        cache_key = 'product_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        try:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60*15)  # Cache the response for 15 minutes
            return response
        except Exception as e:
            return Response({"detail": "An error occurred during product listing."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Token View for user authentication using email and password.
    """
    serializer_class = CustomTokenObtainPairSerializer
