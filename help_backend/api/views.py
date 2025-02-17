
from rest_framework.response import Response
from rest_framework.views import APIView

from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import *
from api.__init__ import *
from .validation import *
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
        with open("test.json", 'w') as jf:
            json.dump(clean_data , jf, indent=4)
        return Response(clean_data, status=S200)
