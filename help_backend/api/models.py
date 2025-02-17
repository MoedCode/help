from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Base(models.Model):
    """Base model with common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField(auto_now_add=True)  # New field for the date only
    updated_date = models.DateField(auto_now=True)  # New field for the date only

    class Meta:
        abstract = True  # This ensures Django does not create a separate table for Base

class Users(AbstractUser, Base):
    """Custom user model that inherits from AbstractUser and Base."""

    # Email, first name, and last name fields, ensuring they're required
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)

    # Profile image field
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
# Linking user to a group
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return self.username

class Group(models.Model):
    """Group that users can belong to."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HelpRequest(models.Model):
    """Help request from a user, sent to other users in the same group."""
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='help_requests')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='help_requests')
    description = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Help Request from {self.user.username} in {self.group.name}"