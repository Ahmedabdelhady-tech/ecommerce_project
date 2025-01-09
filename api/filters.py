import django_filters
from django_filters.rest_framework import FilterSet, NumberFilter, ModelChoiceFilter, BooleanFilter
from products.models import Product, Category

class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte', label='Minimum Price')
    max_price = NumberFilter(field_name='price', lookup_expr='lte', label='Maximum Price')
    category = ModelChoiceFilter(queryset=Category.objects.all())
    stock_available = BooleanFilter(field_name='stock_quantity', lookup_expr='gt', label='In Stock')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'stock_available']

