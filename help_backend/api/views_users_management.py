from api.views_main import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
# Create your views here.
class Hi(APIView):

    def get(self, request):
        return Response(
            {"message":"Help Application Api Routs"} , status=S200
        )

@method_decorator(csrf_exempt, name='dispatch')
class getCSRFCookie(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({"csrf_token": csrf_token})

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

        user.is_active = False;
        user.save()  # Now the password is securely stored

        # 🔹 Create the Profile instance for the user
        Profile.objects.create(user=user)

        # Serialize the user object using UsersSerializer
        serializer = UsersSerializer(user, context={"request": request}).data
        verification = VerificationCode.objects.create(user=user)

        # Write serialized data to test.json for debugging
        return Response({
            "user": serializer,
            "verification_code": verification.code,  # Return Verification Code in Response
            "message": "User registered successfully. Please verify your code.",
            "is_active":user.is_active
        }, status=200)

class GetVerificationCode(APIView):
    def post(self, request):
        username = request.data.get("username")
        mobile_number = request.data.get("mobile_number")

        if not username or not mobile_number:
            return Response(
                {"error": "Username and Mobile Number are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Users.objects.get(username=username, mobile_number=mobile_number)
        except Users.DoesNotExist:
            return Response(
                {"error": "Invalid Username or Mobile Number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Clear expired codes before generating new one
        VerificationCode.clear_codes(user=user)

        # Generate new verification code
        verification_code = VerificationCode.objects.create(user=user)

        return Response(
            {
                "message": "Verification code generated successfully",
                "code": verification_code.code,  # ✅ Show the code (Only for testing)
                "expire_at": verification_code.expire_date.strftime("%Y-%m-%d %H:%M:%S"),
            },
            status=status.HTTP_200_OK
        )

class ActivateAccount(APIView):
    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")

        if not username or not code:
            return Response({"error": "Username and Verification Code are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(username=username)
            verification = VerificationCode.objects.get(user=user, code=code)
        except (Users.DoesNotExist, VerificationCode.DoesNotExist):
            return Response({"error": "Invalid Username or Verification Code"}, status=status.HTTP_400_BAD_REQUEST)

        if verification.is_used:
            return Response({"error": "This verification code is already used"}, status=status.HTTP_400_BAD_REQUEST)

        # Here 🔥
        if timezone.now() > verification.expire_date:
            return Response({"error": "Verification code has expired"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        verification.is_used = True
        verification.save()

        return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)

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

        user_q = Users.objects.filter(username=username).first()
        if not user_q.is_active:
            return Response({"error":"please activate your account"}, S401)
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

            if not user.is_active:
                return Response({"error":"please activate your account"}, S401)
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
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=S400)
        # Authenticate user
        user_q = Users.objects.filter(username=username).first()
        if not check_password(password, user_q.password):
            return Response({"error": "password "}, status=S401)
        if not user_q:
            return Response({"error": "user is not exist"}, status=S401)
        # user = authenticate(username=username, password=password)
        # if not user:
            # return Response({"error": "Invalid credentials"}, status=S401)

        # Ensure the user is deleting their own account
        # if request.user != user:
        #     return Response({"error": "login  required"}, status=S403)

        # Log out the user if they are authenticated
        logout(request)

        # Delete user account
        user_q.delete()

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

        # Data To Update
        update_data = request.data.get("update_data", {})
        N_username = update_data.get("username", "")
        N_email = update_data.get("email", "")
        N_mobile_number = update_data.get("mobile_number", "")

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
        if Users.objects.filter(username=N_username).exists():
            return Response({"error": f"Username{N_username} already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if Users.objects.filter(email=N_email).exists():
            return Response({"error": f"Email {N_email}already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(mobile_number=N_mobile_number).exists():
            return Response({"error": f"mobile_number{N_mobile_number} already exists"}, status=status.HTTP_400_BAD_REQUEST)
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
        if N_mobile_number and user.mobile_number != N_mobile_number:
            user.is_active = False
            user.save()
            VerificationCode.objects.create(user=user)
            return Response({"message": "Mobile number updated. Verification code sent. Please activate your account."}, status=S200)
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
        user_q = Users.objects.filter(username=request.user.username).first()
        if not user_q.is_active:
            return Response({"error":f"{user_q.username}please activate your account"}, S401)
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

        serializer = ProfileSerializer(profile).data
        del serializer["verified"]
        return Response(serializer, status=S200)

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