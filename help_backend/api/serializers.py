from rest_framework import serializers
from api.models import *

class UsersSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["username", "email", "first_name", "last_name", "id"]
        # fields = "__all__"



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile

        fields = "__all__"

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations

        fields = "__all__"
class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups

        fields = "__all__"

class SubscriptionPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPackage

        fields = "__all__"
class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription

        fields = "__all__"
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message

        fields = "__all__"
class HelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest

        fields = "__all__"
classesSerializers = {
    "users":UsersSerializer,
    "users|_all":UsersSerializerAll,
    "profile":ProfileSerializer,
    "locations":LocationsSerializer,
    "groups":GroupsSerializer,
    "help_request":HelpRequestSerializer,
    "message":MessageSerializer,
    "Subscription_packages":SubscriptionPackagesSerializer,
    "user_Subscription":UserSubscriptionSerializer,

}