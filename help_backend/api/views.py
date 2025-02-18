
from rest_framework.response import Response
from rest_framework.views import APIView

from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import *
from api.__init__ import *
from .validation import *
from .serializers import *
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
