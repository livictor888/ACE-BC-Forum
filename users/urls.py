from django.urls import path
from .views import register_user
from .views import signup
from .views import delete_user

app_name = "users"

urlpatterns = [
    path("", register_user, name="create_user"),
    path("delete_user/", delete_user, name="delete_user"),
    path("signup", signup, name="signup"),
]
