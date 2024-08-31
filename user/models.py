from django.db import models
from django.contrib.auth.models import AbstractUser


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
