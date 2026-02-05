from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLES_CHOICES = [
    ('admin', 'Admin'),
    ('sales', 'Sales Executive'),
    ('inventory', 'Inventory Manager'),
]

class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    roles = models.CharField(max_length=20, choices=ROLES_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'roles']

    def __str__(self):
        return f"{self.email} - {self.roles}"