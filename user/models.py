from django.db import models
from django.contrib.auth.models import AbstractUser
from market.models import *

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=[('farmer', 'Farmer'), ('vendor', 'Vendor')])
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    # Add related_name attributes to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change 'user_set' to 'customuser_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change 'user_set' to 'customuser_set'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',)
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='cart_items')
    market_item = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart item: {self.market_item.title} (x{self.quantity})"
    
class Order(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='orders')
    market_item = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.user.username} for {self.market_item.title} (x{self.quantity})"
    