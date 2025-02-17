
from rest_framework.response import Response
from rest_framework.views import APIView

from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from api.__init__ import *
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
