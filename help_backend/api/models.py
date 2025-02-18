from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
time_format = "%Y-%m-%dT%H:%M:%S.%f"

class Base(models.Model):
    """Base model with common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict['id'] = str(new_dict['id'])
        if "created_date" in new_dict:
            new_dict['created_date'] = new_dict['created_date'].strftime(time_format)
        if "updated_date" in new_dict:
            new_dict['updated_date'] = new_dict['updated_date'].strftime(time_format)
        new_dict.pop('_state', None)
        if 'date_joined' in new_dict:
            new_dict['date_joined'] = new_dict['date_joined'].strftime(time_format)

        if 'user_id' in new_dict:
            new_dict['user_id'] = str(new_dict['user_id'])
        return new_dict
    def serializer(self):
        serialized = self.to_dict()
        if 'password' in serialized:
            serialized.pop("password")
        if 'created_date' in serialized:
            serialized.pop("created_date")
        if 'updated_date' in serialized:
            serialized.pop("updated_date")
        return serialized

class Group(models.Model):
    """Group that users can belong to."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    """Model to store location details."""
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.address if self.address else f"{self.latitude}, {self.longitude}"


class Users(AbstractUser, Base):
    """Custom user model that inherits from AbstractUser and Base."""

    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)

    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    # New fields
    mobile_number = models.CharField(max_length=15, unique=True, blank=False, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Address fields (separate from Location)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    # User's last known location
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")

    REQUIRED_FIELDS = ["email", "first_name", "last_name", "mobile_number"]

    def __str__(self):
        return self.username
class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to="profile_images",
        default="profile_images/blank-profile-picture.png",
    )
    profession = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



class HelpRequest(models.Model):
    """Help request from a user, sent to other users in the same group."""
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='help_requests')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='help_requests')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="help_requests")
    description = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Help Request from {self.user.username} in {self.group.name}"


class Message(models.Model):
    """Model to handle user-to-user messaging."""
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_messages')
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"
