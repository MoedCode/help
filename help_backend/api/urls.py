from django.urls import path
from . import views

urlpatterns = [
    path("hi", views.Hi.as_view(), name="hi"),
    path("csrf", views.getCSRFCookie.as_view(), name="csrf"),
    path("register/", views.Register.as_view(), name="resgister"),


]