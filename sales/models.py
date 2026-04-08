from django.db import models
from django.conf import settings
from leads.models import Customer
from inventory.models import Product

User = settings.AUTH_USER_MODEL

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name="orders")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot price

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"