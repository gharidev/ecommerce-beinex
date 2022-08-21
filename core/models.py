from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# CUSTOM USER MODEL
class User(AbstractUser):
    """Custom user model."""
    class Types(models.TextChoices):
        MANAGER = 'MANAGER', 'Manager'
        CUSTOMER = 'CUSTOMER', 'Customer'

    type = models.CharField('Type', max_length=50, choices=Types.choices, default=Types.CUSTOMER)
    email = models.EmailField(
        'Email address',
        unique=True,
        error_messages={
            "unique": "A user with that email address already exists.",
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_manager(self):
        return self.type == User.Types.MANAGER
    
    @property
    def is_customer(self):
        return self.type == User.Types.CUSTOMER

# USER MANAGERS
class ManagerManager(UserManager):
    """User manager for `Manager`."""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MANAGER)

class CustomerManager(UserManager):
    """User manager for `Customer`."""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)

# PROXY USER MODELS
class Manager(User):
    """Proxy user model for managers."""
    class Meta:
        proxy = True

    objects = ManagerManager

class Customer(User):
    """Proxy user model for customers"""
    class Meta:
        proxy = True

    objects = CustomerManager

# PRODUCT & CATEGORY MODEL
class Product(models.Model):
    """Product model."""

    PLACEHOLDER_URL = 'https://www.slntechnologies.com/wp-content/uploads/2017/08/ef3-placeholder-image.jpg'

    name = models.CharField(max_length=255)
    # image = models.ImageField(default='placeholder-image.webp', blank=True, upload_to='media/images')
    # Using URLField as Heorku has an ephemeral filesystem
    image = models.URLField(default=PLACEHOLDER_URL, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField('Category', blank=True)
    subcategories = models.ManyToManyField('SubCategory', blank=True)

    @property
    def categories_str(self):
        return ', '.join([c.name for c in self.categories.all()])
    
    @property
    def subcategories_str(self):
        return ', '.join([c.name for c in self.subcategories.all()])

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = Product.image.field.default
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['pk']

class Category(models.Model):
    """Category model."""
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['pk']
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    """SubCategory model."""
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "sub categories"
        ordering = ['pk']
    
    def __str__(self):
        return self.name