from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user used exclusively for the FutureForge Labs admin dashboard.
    Public site visitors never need an account.
    """
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('editor', 'Content Editor'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='editor')
    phone_number = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='accounts/avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ff_users'

    def __str__(self):
        return self.get_full_name() or self.username
