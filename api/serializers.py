from rest_framework import serializers
from products.models import Product, Category
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model to handle category-related data.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model to handle product-related data.
    - Includes category data (read-only) and category_id (write-only).
    """
    category = CategorySerializer(read_only=True)  # Nested Category serializer (read-only)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )  # category_id is a write-only field that maps to the category

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id', 
                  'stock_quantity', 'image_url', 'created_date']
        read_only_fields = ['id', 'created_date', 'stock_quantity']  # Fields that are read-only

    def validate_category_id(self, value):
        """
        Ensure the category_id is valid and exists in the database.
        """
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value

    def validate_price(self, value):
        """
        Ensure the price is a positive value.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock_quantity(self, value):
        """
        Ensure the stock quantity is non-negative.
        """
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token serializer for JWT authentication using email and password.
    This overrides the default behavior of TokenObtainPairSerializer to authenticate users via email.
    """
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Use Django's authenticate method to validate user credentials
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid credentials.")
        
        if not user.is_active:
            raise AuthenticationFailed("User account is not active.")
            
        # If all checks pass, add the username to the attributes
        attrs['username'] = user.username
        
        # Return the validated data by calling the parent class method
        return super().validate(attrs)
