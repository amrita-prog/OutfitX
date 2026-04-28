from django.db import models
from sales.models import Order


class Invoice(models.Model):
    STATUS_CHOICES = (
        ('generated', 'Generated'),
        ('paid', 'Paid'),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='invoice'
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='generated'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} - Order #{self.order.id}"
    



class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('cash', 'Cash'),
    )

    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.id} - Invoice #{self.invoice.id}"