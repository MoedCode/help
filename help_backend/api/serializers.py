from rest_framework import serializers
from api.models import *
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        # fields = ["username", "email", "first_name", "last_name", "profile_image"]
        fields = "__all__"
