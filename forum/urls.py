from django.urls import path
from .views import AdvancedSearch, PostList, PostDetail, PostCreate, MonthList, YearList, Search, DeletePost, EditPost, AdvSearchResult, EditCommentView, DeleteComment, EditCommentReplyView, DeleteCommentReply

app_name = "forum"

urlpatterns = [

    # uncomment the path below for to test a list of all posts at /list
    # path("list/", PostList.as_view(), name="list"),
    path("<int:pk>/", PostDetail.as_view(), name="detail"),
    path("new/", PostCreate.as_view(), name="create"),
    path("year/<int:year>/", MonthList.as_view(), name="monthlist"),
    path("year/<int:year>/<int:month>/", PostList.as_view(), name="archive"),
    path("year/<int:year>/<int:month>/<int:page>", PostList.as_view(), name="archive-by-page"),
    path("year/", YearList.as_view(), name="yearlist"),
    path("", YearList.as_view(), name="yearlist"),
    path("search/", PostList.as_view(), name="list"),
    path("search/<str:search>/", Search.as_view(), name="search"),
    path("search/<str:search>/<int:page>", Search.as_view(), name="search-by-page"),
    path("delete_post/<int:pk>", DeletePost.as_view(), name="deletepost"),
    path("edit_post/<int:pk>", EditPost.as_view(), name="editpost"),
    path("advsearch/", AdvancedSearch.as_view(), name="advancedSearch"),
    path('advsearch/result/', AdvSearchResult.as_view(), name='adv-search-result'),
    path('<int:post_pk>/edit_comment/<int:comment_pk>/', EditCommentView.as_view(), name='edit_comment'),
    path('<int:post_pk>/delete_comment/<int:comment_pk>/', DeleteComment.as_view(), name='delete_comment'),
    path('<int:post_pk>/edit_comment_reply/<int:comment_reply_pk>/', EditCommentReplyView.as_view(), name='edit_comment_reply'),
    path('<int:post_pk>/delete_comment_reply/<int:comment_reply_pk>/', DeleteCommentReply.as_view(), name='delete_comment_reply'),
]