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


class Users(AbstractUser, Base):
    """Custom user model that inherits from AbstractUser and Base."""

    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)

    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    # group = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    group = models.ForeignKey("api.Groups", on_delete=models.SET_NULL, null=True, blank=True, related_name="user_groups")


    # New fields
    mobile_number = models.CharField(max_length=15, unique=True, blank=False, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Address fields (separate from Locations)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    # User's last known location
    # location = models.OneToOneField(Locations, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")
    location = models.ForeignKey("api.Locations", on_delete=models.SET_NULL, null=True, blank=True, related_name="user_location")

    REQUIRED_FIELDS = ["email", "first_name", "last_name", "mobile_number"]

    def __str__(self):
        return self.username
class Locations(models.Model):
    """Model to store location details and associate it with a user."""
    # user = models.OneToOneField(
    #     Users, on_delete=models.CASCADE, related_name="location"
    # )
    user = models.ForeignKey("api.Users", on_delete=models.CASCADE, related_name="user_location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Locations of {self.user.username} - {self.address or f'{self.latitude}, {self.longitude}'}"
class Groups(models.Model):
    """Groups that users can belong to."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    admin_user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="admin_groups"
    )

    # members = models.ManyToManyField(Users, related_name="groups", blank=True)
    members = models.ManyToManyField("api.Users", related_name="user_groups")

    def add_member(self, user):
        """Admin can add users to the group."""
        if user not in self.members.all():
            self.members.add(user)

    def remove_member(self, user):
        """Admin can remove users from the group."""
        if user in self.members.all():
            self.members.remove(user)

    def assign_new_admin(self, new_admin):
        """Admin can assign another user as the admin."""
        if new_admin in self.members.all():
            self.admin_user = new_admin
            self.save()

    def user_exit(self, user):
        """Allows a user to leave the group, transferring admin if needed."""
        if user == self.admin_user:
            members = list(self.members.all())  # Get all members
            if members:  # If other users exist, assign first member as admin
                self.admin_user = members[0]
            else:  # If no members left, delete the group
                self.delete()
                return
        self.members.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} (Admin: {self.admin_user.username})"


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
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='help_requests')
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True, blank=True, related_name="help_requests")
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

Classes = {
    "Users":Users,
    "Profile":Profile,
    "Locations":Locations,
    "HelpRequest":HelpRequest,
    "Message":Message,

}
classes = {
    "users":Users,
    "profile":Profile,
    "locations":Locations,
    "helpRequest":HelpRequest,
    "message":Message,

}