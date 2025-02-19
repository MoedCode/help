
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,  logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, generics
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

            # Get CSRF token
            csrf_token = get_token(request)

            # Create response
            response = Response(
                {"message": "Login successful", "user": {"username": user.username}},
                status=S200
            )

            # Set session ID and CSRF token in cookies
            response.set_cookie(key="sessionid", value=request.session.session_key, httponly=True, secure=False, samesite="Lax")
            response.set_cookie(key="csrftoken", value=csrf_token, secure=False, samesite="Lax")

            return response
        else:
            return Response({"error": "Invalid credentials"}, status=S401)

class Logout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=S200)

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

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            username = request.data.get("username")
            user = Users.objects.filter(username=username).first()
            profile = Profile.objects.filter(user=user).first()
            serialized_profile = ProfileSerializer(profile, context={"request": request})
            return Response(
                serialized_profile, status=S200
            )
        except Exception as e:
            return Response(
                {"error":str(e)}, status=S500
            )


class AddUserToGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group_identifier = request.data.get("group_name") or request.data.get("group_id")
        admin_username = request.data.get("admin_username")
        add_username = request.data.get("add_username")

        # Validate input
        if not all([group_identifier, admin_username, add_username]):
            return Response({"error": "Missing required fields"}, status=S400)

        # Check if admin user exists
        admin_user = Users.objects.filter(username=admin_username).first()
        if not admin_user or not admin_user.is_authenticated:
            return Response({"error": "Invalid or unauthenticated admin user"}, status=S401)

        # Find the group by name or ID
        group = None
        if isinstance(group_identifier, int):  # If group_id is given
            group = Groups.objects.filter(id=group_identifier).first()
        else:  # If group_name is given
            group = Groups.objects.filter(name=group_identifier).first()

        if not group:
            return Response({"error": "Group not found"}, status=S404)

        # Check if admin user is the group's admin
        if group.admin_user != admin_user:
            return Response({"error": "Only the group admin can add users"}, status=S403)

        # Check if the user to be added exists
        add_user = Users.objects.filter(username=add_username).first()
        if not add_user:
            return Response({"error": "User to be added not found"}, status=S404)

        # Add user to group
        group.members.add(add_user)
        return Response({"message": f"{add_username} added to {group.name} successfully"}, status=S200)
class RemoveUserFromGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"\n\nrequest header\n\n")
        group_identifier = request.data.get("group_name") or request.data.get("group_id")
        admin_username = request.data.get("admin_username")
        remove_username = request.data.get("remove_username")

        # Validate input
        if not all([group_identifier, admin_username, remove_username]):
            return Response({"error": "Missing required fields"}, status=S400)

        # Check if admin user exists and is authenticated
        admin_user = Users.objects.filter(username=admin_username).first()
        if not admin_user or not admin_user.is_authenticated:
            return Response({"error": "Invalid or unauthenticated admin user"}, status=S401)

        # Find the group by name or ID
        group = None
        if isinstance(group_identifier, int):  # If group_id is given
            group = Groups.objects.filter(id=group_identifier).first()
        else:  # If group_name is given
            group = Groups.objects.filter(name=group_identifier).first()

        if not group:
            return Response({"error": "Group not found"}, status=S404)

        # Check if admin user is the group's admin
        if group.admin_user != admin_user:
            return Response({"error": "Only the group admin can remove users"}, status=S403)

        # Check if the user to be removed exists
        remove_user = Users.objects.filter(username=remove_username).first()
        if not remove_user:
            return Response({"error": "User to be removed not found"}, status=S404)

        # Check if the user is in the group
        if remove_user not in group.members.all():
            return Response({"error": "User is not a member of this group"}, status=S400)

        # Remove user from group
        group.members.remove(remove_user)
        return Response({"message": f"{remove_username} removed from {group.name} successfully"}, status=S200)
class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=S400)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=S401)

        # Ensure the user is deleting their own account
        if request.user != user:
            return Response({"error": "You can only delete your own account"}, status=S403)

        # Log out the user if they are authenticated
        logout(request)

        # Delete user account
        user.delete()

        return Response({"message": "Account deleted successfully"}, status=S200)
