from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Unique identifier for the product
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock_quantity = models.PositiveIntegerField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (SKU: {self.sku or 'N/A'})"

    def reduce_stock(self, quantity):
        """
        Reduces the stock quantity of the product.
        Returns True if successful, False if not enough stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False

    def save(self, *args, **kwargs):
        """
        Override save method to automatically generate SKU if not provided.
        """
        if not self.sku:
            self.sku = f"SKU-{self.name[:3].upper()}-{self.id or ''}"
        super().save(*args, **kwargs)
