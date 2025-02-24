from datetime import datetime
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
time_format = "%Y-%m-%dT%H:%M:%S.%f"

time_format = "%Y-%m-%d %H:%M:%S"  # Format: YYYY-MM-DD HH:MM:SS

class Base(models.Model):
    """Base model with common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(default=timezone.now, editable=False)  # ✅ Immutable, defaults to now
    updated_date = models.DateTimeField(auto_now=True)  # ✅ Auto-updates on modification

    class Meta:
        abstract = True  # ✅ Ensures Django doesn't create a `Base` table

    def to_save(self, *args, **kwargs):
        """Prevent modification of created_date"""
        if self.pk:  # If object exists, prevent modification of created_date
            old_instance = self.__class__.objects.get(pk=self.pk)
            self.created_date = old_instance.created_date  # Keep original value
        super().save(*args, **kwargs)

    def to_dict(self):
        """Convert model instance to dictionary, formatting date fields."""
        new_dict = self.__dict__.copy()
        new_dict['id'] = str(new_dict['id'])
        new_dict['created_date'] = self.created_date.strftime(time_format)
        new_dict['updated_date'] = self.updated_date.strftime(time_format)
        new_dict.pop('_state', None)  # Remove internal Django state

        if 'date_joined' in new_dict:
            new_dict['date_joined'] = new_dict['date_joined'].strftime(time_format)

        if 'user_id' in new_dict:
            new_dict['user_id'] = str(new_dict['user_id'])

        return new_dict

    def inttant_serializer(self):
        """Convert instance to dictionary but hide sensitive fields."""
        serialized = self.to_dict()
        for field in ["password", "created_date", "updated_date"]:
            serialized.pop(field, None)  # ✅ Safely remove sensitive fields
        return serialized

class Users(AbstractUser, Base):
    """Custom user model that inherits from AbstractUser and Base."""

    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)

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
class Locations(Base):
    """Model to store location details and associate it with a user."""

    user = models.ForeignKey("api.Users", on_delete=models.CASCADE, related_name="user_location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    @classmethod
    def recent(cls, user_id, date_attr_name="updated_date"):
        """
        Get the most recent location for the given user_id based on updated_at timestamp.
        """
        if "updated" in date_attr_name:
            return cls.objects.filter(user_id=user_id).order_by("-updated_date").first()

        if "created" in date_attr_name:
            return cls.objects.filter(user_id=user_id).order_by("-created_date").first()

    def __str__(self):
        return f"Locations of {self.user.username} - {self.address or f'{self.latitude}, {self.longitude}'}"


class Groups(Base):
    """Groups that users can belong to."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

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
class GroupContact(models.Model):
    """Tracks a user's membership in a group with a custom nickname."""

    user = models.ForeignKey(
        "api.Users",
        on_delete=models.SET_NULL,  # Set to NULL instead of deleting the GroupMember instance
        null=True,
        blank=True,
        related_name="group_memberships"
    )
    group = models.ForeignKey(
        "api.Groups",
        on_delete=models.CASCADE,  # If the group is deleted, delete all memberships
        related_name="group_members"
    )
    contact_name = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Custom name in this group

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "group"],
                name="unique_user_in_group",
            )
        ]


    def __str__(self):
        if self.user:
            return f"{self.nickname or self.user.username} in {self.group.name}"
        return f"Deleted Account in {self.group.name}"  # If the user is deleted


class Profile(Base):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images",
        default="profile_images/blank-profile-picture.png",
    )
    profession = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)



    def __str__(self):
        return self.user.username



class HelpRequest(Base):
    """Help request from a user, sent to other users in the same group."""
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='help_requests')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='help_requests')
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True, blank=True, related_name="help_requests")
    description = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Help Request from {self.user.username} in {self.group.name}"


class Message(Base):
    """Model to handle user-to-user messaging."""
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_messages')
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"

class SubscriptionPackage(Base):
    """Subscription package model for different subscription plans."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Subscription cost
    duration_days = models.PositiveIntegerField()  # Duration in days (e.g., 30 for monthly, 365 for yearly)

    created_by = models.ForeignKey(
        "api.Users",  # String reference to avoid circular imports
        on_delete=models.CASCADE,
        related_name="created_packages",
        limit_choices_to={'is_superuser': True},  # Ensures only superusers (admins) can create packages
    )

    def __str__(self):
        return f"{self.name} - ${self.price} ({self.duration_days} days)"


class UserSubscription(Base):
    """User subscription model to track which users have which subscriptions."""
    user = models.ForeignKey(
        "api.Users",  # String reference to avoid circular imports
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )
    package = models.ForeignKey(
        "api.SubscriptionPackage",  # String reference to SubscriptionPackage
        on_delete=models.CASCADE,
        related_name="user_subscriptions"
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()  # Expiry date based on package duration

    def save(self, *args, **kwargs):
        """Automatically calculate end date based on package duration before saving."""
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.package.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.package.name} until {self.end_date.strftime('%Y-%m-%d')}"

class UserConnections(Base):
    """Model to store user connections, including joined groups and trusted contacts."""
    user = models.ForeignKey(
        "api.Users",  # Reference to the user who owns these connections
        on_delete=models.CASCADE,
        related_name="connections"
    )
    group_name = models.CharField(max_length=255, blank=True, null=True)  # Name of the joined group
    contact_name = models.CharField(max_length=255)  # Name of the trusted contact
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Primary phone number
    additional_phone_numbers = models.JSONField(blank=True, null=True)  # Store multiple phone numbers as JSON
    email = models.EmailField(blank=True, null=True)  # Contact's email
    address = models.TextField(blank=True, null=True)  # Optional address field
    notes = models.TextField(blank=True, null=True)  # Additional notes for the contact

    def __str__(self):
        return f"{self.user.username}'s Contact: {self.contact_name} ({self.phone_number})"


Classes = {
    "Users":Users,
    "Profile":Profile,
    "Locations":Locations,
    "Groups":Groups,
    "HelpRequest":HelpRequest,
    "Message":Message,
    "SubscriptionPackage":SubscriptionPackage,
    "UserSubscription":UserSubscription,
    "UserConnections":UserConnections,
}
classes = {
    "users":Users,
    "profile":Profile,
    "locations":Locations,
    "groups":Groups,
    "helpRequest":HelpRequest,
    "message":Message,
    "subscription_package":SubscriptionPackage,
    "user_subscription":UserSubscription,
    "user_connections":UserConnections,
}