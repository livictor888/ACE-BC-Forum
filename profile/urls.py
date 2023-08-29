from django.urls import path
from .views import ProfilePage
from .views import EditProfile

app_name = "profile"

urlpatterns = [
    path("", ProfilePage.as_view(), name="profile"),
    path("edit", EditProfile.as_view(), name="edit_profile"),
]
