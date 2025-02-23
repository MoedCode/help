from django.urls import path
from . import views

urlpatterns = [
    path("", views.Hi.as_view(), name="about"),
    # path("csrf", views.getCSRFCookie.as_view(), name="csrf"),
                        #Users URL's
    path("register/", views.Register.as_view(), name="resgister"),
    path("delete_user/", views.DeleteUser.as_view(), name="delete_user"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("login/", views.Login.as_view(), name="login"),
    path("user_data/", views.GetUserData.as_view(), name="user_data"),
    path("user_update/", views.UserUpdate.as_view(), name="user_update"),

                        #Profile URL's
    path("profile_view/", views.ProfileView.as_view(), name="profile_view"),
    path("profile_update/", views.ProfileUpdate.as_view(), name="profile_update"),

                        #Groups URL's
    path("create_group/", views.CreateGroup.as_view(), name="create_group"),
    path("add_user_to_group/", views.AddUserToGroup.as_view(), name="add_user_to_group"),
    path("remove_user_from_group/", views.RemoveUserFromGroup.as_view(), name="remove_user_from_group"),

                        # Location URL's
    path("set_location/", views.SetLocations.as_view(), name="set_location"),
    path("set_location/<str:id>/", views.SetLocations.as_view(), name="set_location_detail"),
    path("get_locations/", views.SetLocations.as_view(), name="get_locations"),
    path("get_location/", views.RecentLcation.as_view(), name="get_locations"),
    path("update_location/", views.SetLocations.as_view(), name="update_location"),
    path("delete_location/<str:id>/", views.SetLocations.as_view(), name="delete_location"),
    path("delete_location/", views.SetLocations.as_view(), name="delete_location"),
    path("delete_all_locations/", views.DeleteAllLocations.as_view(), name="delete_all_locations"),
    path("subscription/", views.SubscriptionPackageView.as_view(), name="subscription"),
                        # echo request
    path("echo_request/", views.EchoRequestView.as_view(), name="echo_request"),
]