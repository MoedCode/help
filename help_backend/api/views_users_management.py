from api.views_main import *


# Create your views here.
class Hi(APIView):

    def get(self, request):
        return Response(
            {"message":"its kaky"} , status=S200
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
        username = clean_data.get("username")
        email = clean_data.get("email")
        mobile_number = clean_data.get("mobile_number")

        # Check if the username or email already exists
        if Users.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if Users.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(mobile_number=mobile_number).exists():
            return Response({"error": "mobile_number already exists"}, status=status.HTTP_400_BAD_REQUEST)
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
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
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
            # csrf_token = get_token(request)

            # Create response
            return  Response(
                {"message": "Login successful", "user": {"username": user.username}},
                status=S200
            )

            # # Set session ID and CSRF token in cookies
            # response.set_cookie(key="sessionid", value=request.session.session_key, httponly=True, secure=False, samesite="Lax")
            # response.set_cookie(key="csrftoken", value=csrf_token, secure=False, samesite="Lax")

            # return response
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
            return Response({"error": "login  required"}, status=S403)

        # Log out the user if they are authenticated
        logout(request)

        # Delete user account
        user.delete()

        return Response({"message": "Account deleted successfully"}, status=S200)
class GetUserData(APIView):
    permission_classes = [IsAuthenticated]  # Ensure authentication is required

    def post(self, request):
        # Extract username and password from request body
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials."}, status=401)

        # Ensure the authenticated user matches the logged-in user
        if request.user != user:
            return Response({"error": "Unauthorized access."}, status=403)

        # Fetch user and profile data
        user_data = UsersSerializer(user).data
        profile = Profile.objects.filter(user=user).first()
        profile_data = ProfileSerializer(profile).data if profile else {}

        return Response({
            "user": user_data,
            "profile": profile_data
        })
class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def put(self, request):
        # Extract username, password, and update_data from request body
        username = request.data.get("username")
        password = request.data.get("password")
        update_data = request.data.get("update_data", {})

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=S400)

        if not update_data:
            return Response({"error": "No update data provided."}, status=S400)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials."}, status=S401)

        # Ensure the authenticated user matches the logged-in user
        if request.user != user:
            return Response({"error": "Unauthorized access."}, status=S403)

        try:
            # Validate the update data
            cleaned_data = validate_user_data(update_data)
        except ValidationError as e:
            return Response({"error": e.detail}, status=S400)

        # Check if password is being updated
        new_password = cleaned_data.pop("password", None)

        # Update user fields
        for field, value in cleaned_data.items():
            setattr(user, field, value)

        # Handle password update separately
        if new_password:
            user.set_password(new_password)
            user.save()
            logout(request)  # Log out the user after password change
            return Response({"message": "Password updated successfully. Please log in again."}, status=S200)
        user.is_active = False
        user.save()

        # Serialize and return updated user data
        serializer = UsersSerializer(user)
        return Response({"message": "User data updated successfully.", "user": serializer.data}, status=S200)

class ProfileUpdate(APIView):
    """ Profile Update Endpoint Class """
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def put(self, request):
        is_valid, result = validate_profile_update(request.data)
        if not is_valid:
            return Response(result, status=S400)

        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            try:
                profile = Profile.objects.create(user=request.user)
            except Exception as e:
                return Response({"error": str(e)}, status=S500)

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profileimg']

        # Update other fields
        for field, value in result.items():
            setattr(profile, field, value)
        profile.save()

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=S200)

class profileUpdate_(APIView):
    """ Pofile Update Endpoint Class"""
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    def put(self, request):
        is_valid , result = validate_profile_update(request.data)
        if not is_valid:
            return Response(result, S400)
        # if request.user.is_auth:
        #     return Response({"error": "Unauthorized access."}, status=S403)

        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            try:
                profile = Profile.objects.create(user=request.user)
            except Exception as e:
                return Response({"error":str(e)}, S500)
        for field, value in result.items():
            setattr(profile, field, value)
        profile.save()
        serializer = ProfileSerializer(profile).data
        return Response(serializer, S200)


"""
class Search(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # try:
        category = request.data.get("category")
        key = request.data.get("key")
        value = request.data.get("value")

        category = category.lower()
        query = {key:value}

        if category not in classes.keys():
            return Response({"errror":f"category {category} is not exxist "}, S404)
        if category in ["user", "users"]:
            user = Users.objects.filter(**query).first()
            if not user:
                return Response({"error":f"cant find user {value}"}, status=S404)
            if request.user != user:
                return Response({"error": "not authorized"}, status=S401)
            serial_user = UsersSerializer(user, context={"request": request}).data
            print(f"\n\n\n {serial_user} \n\n\n")

            return Response(serial_user, status=S200)
        # try:
        Class = classes[category]
        ClassSerializor = classesSerializers[category]
        queryObjt = Class.objects.filter(**query).first()
        serializedObject = ClassSerializor(queryObjt, context={"request":request})
        return Response(serializedObject, S200)
        # except Exception as e:
            # return Response({"error":str(e)})
        # except Exception as e:
        #     return Response({"error":str(e)}, S400)
"""

'''
class Search(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        category = request.data.get("category", "").lower()
        key = request.data.get("key")
        value = request.data.get("value")

        if not category or not key or value is None:
            return Response({"error": "Missing required fields (category, key, or value)."}, S400)

        search_methods = {
            "user": self.search_user,
            "users": self.search_user,
            "profile": self.search_profile,
            "profiles": self.search_profile,
            "group": self.search_group,
            "groups": self.search_group,
            "message": self.search_message,
            "messages": self.search_message,
        }

        if category not in search_methods:
            return Response({"error": f"Category '{category}' does not exist."}, S404)

        return search_methods[category](request, key, value)

    def search_user(self, request, key, value):
        """Search for a user, ensuring the requester can only access their own data."""
        try:
            user = Users.objects.filter(**{key: value}).first()
            if not user:
                return Response({"error": f"User '{value}' not found."}, S404)

            if request.user != user:
                return Response({"error": "Not authorized to view this user."}, S403)

            serialized_user = UsersSerializer(user, context={"request": request}).data
            return Response(serialized_user, S200)
        except FieldError:
            return Response({"error": f"Invalid search key '{key}' for Users."}, S400)

    def search_profile(self, request, key, value):
        """Search for a profile linked to the requesting user."""
        try:
            profile = Profile.objects.filter(user=request.user, **{key: value}).first()
            if not profile:
                return Response({"error": f"Profile '{value}' not found."}, S404)

            serialized_profile = ProfileSerializer(profile, context={"request": request}).data
            return Response(serialized_profile, S200)
        except FieldError:
            return Response({"error": f"Invalid search key '{key}' for Profile."}, S400)

    def search_group(self, request, key, value):
        """Search for a group (users can search for groups they belong to)."""
        try:
            group = Groups.objects.filter(members=request.user, **{key: value}).first()
            if not group:
                return Response({"error": f"Group '{value}' not found or you are not a member."}, S404)

            serialized_group = GroupsSerializer(group, context={"request": request}).data
            return Response(serialized_group, S200)
        except FieldError:
            return Response({"error": f"Invalid search key '{key}' for Group."}, S400)

    def search_message(self, request, key, value):
        """Search for messages where the requester is the sender or receiver."""
        try:
            message = Message.objects.filter(
                sender=request.user, **{key: value}
            ).first() or Message.objects.filter(
                receiver=request.user, **{key: value}
            ).first()

            if not message:
                return Response({"error": f"Message '{value}' not found."}, S404)

            serialized_message = MessageSerializer(message, context={"request": request}).data
            return Response(serialized_message, S200)
        except FieldError:
            return Response({"error": f"Invalid search key '{key}' for Message."}, S400)

'''