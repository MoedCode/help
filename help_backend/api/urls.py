from django.urls import path
from . import views

urlpatterns = [
    path("", views.Hi.as_view(), name="about"),
    path("csrf", views.getCSRFCookie.as_view(), name="csrf"),
                        #Users URL's
    path("register/", views.Register.as_view(), name="resgister"),
    path("delete_user/", views.DeleteUser.as_view(), name="delete_user"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("login/", views.Login.as_view(), name="login"),
    path("user_data/", views.GetUserData.as_view(), name="user_data"),
    path("user_update/", views.UserUpdate.as_view(), name="user_update"),
    path("activate/", views.ActivateAccount.as_view(), name="activate"),
    path("get_code/", views.GetVerificationCode.as_view(), name="get_code"),


                        #Profile URL's
    path("profile_view/", views.ProfileView.as_view(), name="profile_view"),
    path("profile_update/", views.ProfileUpdate.as_view(), name="profile_update"),

                        #Groups URL's
    # path("user_members/<str:group_ID>", views.GroupMembersData.as_view(), name="user_members"),
    path("group_members/", views.GroupMembersData.as_view(), name="group_members"),
    path("user_groups/", views.GetUserGroups.as_view(), name="user_groups"),
    path("create_group/", views.CreateGroup.as_view(), name="create_group"),
    path("update_group/", views.UpdateGroup.as_view(), name="update_group"),
    path("add_user_to_group/", views.AddUserToGroup.as_view(), name="add_user_to_group"),
    path("remove_user_from_group/", views.RemoveUserFromGroup.as_view(), name="remove_user_from_group"),
    path("get_group_contacts/", views.GetUpdateGroupContacts.as_view(), name="get_group_contacts"),

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
                        # HELP request
    path("help/<str:msg>", views.SendHelpToGroupMembers.as_view(), name="help"),
    path("help/", views.SendHelpToGroupMembers.as_view(), name="help2"),
    path("send/", views.SendEmailToTest.as_view(), name="send"),
    path('send-sms/', views.SendSMSView.as_view(), name='send-sms'),
                        # echo request
    path("echo_request/", views.EchoRequestView.as_view(), name="echo_request"),
]