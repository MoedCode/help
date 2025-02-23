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
from django.core.exceptions import FieldError
ensure_csrf = method_decorator(ensure_csrf_cookie)