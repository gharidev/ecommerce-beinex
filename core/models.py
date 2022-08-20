from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# CUSTOM USER MODEL
class User(AbstractUser):
    """Custom user model."""
    class Types(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'

    type = models.CharField('Type', max_length=50, choices=Types.choices, default=Types.CUSTOMER)

# USER MANAGERS
class AdminManager(UserManager):
    """User manager for `Admin`."""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ADMIN)

class CustomerManager(UserManager):
    """User manager for `Customer`."""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)

# PROXY USER MODELS
class Admin(User):
    """Proxy user model for administrators."""
    class Meta:
        proxy = True

    objects = AdminManager

class Customer(User):
    """Proxy user model for customers"""
    class Meta:
        proxy = True

    objects = CustomerManager

# PRODUCT & CATEGORY MODEL
class Product(models.Model):
    """Product model."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField('Category')
    subcategories = models.ManyToManyField('SubCategory')

class Category(models.Model):
    """Category model."""
    name = models.CharField(max_length=255)

class SubCategory(models.Model):
    """SubCategory model."""
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)