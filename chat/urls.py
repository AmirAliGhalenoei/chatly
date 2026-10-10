from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("group/<uuid:room_id>/", views.GroupChatView.as_view(), name="group_chat"),
    path("privat/<uuid:user_id>/", views.PrivatChatView.as_view(), name="privat_chat"),
    path("create-group/",views.CreateGroupView.as_view(), name="create_group"),
    path("profile/<uuid:user_id>/", views.UserProfileView.as_view(), name="profile"),
    path("edit-profile/<uuid:user_id>/", views.EditProfileView.as_view(), name="edit_profile"),
]