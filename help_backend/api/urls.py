from django.urls import path
from . import views

urlpatterns = [
    path("hi", views.Hi.as_view(), name="hi"),
    path("csrf", views.getCSRFCookie.as_view(), name="csrf"),
    path("register/", views.Register.as_view(), name="resgister"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("login/", views.Login.as_view(), name="login"),
    path("profile_view/", views.ProfileView.as_view(), name="profile_view"),
    path("create_group/", views.CreateGroup.as_view(), name="create_group"),
    path("add_user_to_group/", views.AddUserToGroup.as_view(), name="add_user_to_group"),

]