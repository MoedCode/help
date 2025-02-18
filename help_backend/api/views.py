
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated
from .models import *
from api.__init__ import *
from .validation import *
from .serializers import *
from django.contrib.auth.models import AnonymousUser
import json
ensure_csrf = method_decorator(ensure_csrf_cookie)
# Create your views here.
class Hi(APIView):

    def get(self, request):
        return Response(
            {"mmessage":"its kaky"} , status=S200
        )
class getCSRFCookie(APIView):
    permission_classes = []
    authentication_classes = []

    @ensure_csrf
    def get(self, request):
        return Response({"csrfToken": get_token(request)})
class Register(APIView):
    def post(self, request):
        clean_data = validate_user_data(request.data)

        # Extract password before passing to model
        password = clean_data.pop("password", None)

        # Create user instance (without password)
        user = Users(**clean_data)

        # Hash the password properly
        if password:
            user.set_password(password)  # 🔑 Hashes the password

        user.save()  # Now the password is securely stored

        # 🔹 Create the Profile instance for the user
        Profile.objects.create(user=user)

        # Serialize the user object using UsersSerializer
        serializer = UsersSerializer(user, context={"request": request})

        # Write serialized data to test.json for debugging
        with open("test.json", 'w') as jf:
            json.dump(serializer.data, jf, indent=4)

        return Response(serializer.data, status=S200)

class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Check if both fields are provided
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=S400)

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # Start session
            serializer = UsersSerializer(user, context={"request": request})
            return Response({"message": "Login successful", "user": serializer.data}, status=S200)
        else:
            return Response({"error": "Invalid credentials"}, status=S401)

class CreateGroup(APIView):
    permission_classes = [IsAuthenticated]

class CreateGroup(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        group_name = request.data.get("group_name")
        group_description = request.data.get("group_description")

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None or isinstance(user, AnonymousUser):
            return Response({"error": "Invalid username or password"}, status=S401)

        # Check if user is logged in
        if not request.user.is_authenticated:
            return Response({"error": "User must be logged in"}, status=S403)

        # Create new group
        group = Groups.objects.create(
            name=group_name,
            description=group_description,
            admin_user=user  # Assuming the Group model has an 'admin' field
        )
        group.members.add(user)  # Add user as a member
        return Response({"message": "Group created successfully", "group_id": group.id}, status=S201)
