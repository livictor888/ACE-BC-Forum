from django.urls import path
from .views import PostDetail, PostList, PostCreate

#THIS URLS for pages is not being in use unless you need it

app_name = "pages"


urlpatterns = [
    path("", PostList.as_view(), name="list"),
    path("<int:pk>/", PostDetail.as_view(), name="detail"),
    path("new/", PostCreate.as_view(), name="create"),
]
