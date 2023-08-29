from django.shortcuts import render
import datetime
from django.db.models import Q
from forum.models import Post  # forum_post table
from django.contrib.auth.decorators import login_required

from django.views.generic import (DetailView)
from forum.models import Post, Image, Comment, UploadPDF
from forum.forms import NewCommentForm
from django.shortcuts import render, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def Homepage(request):
    current_datetime = datetime.datetime.now()
    page = request.GET.get('page', 1)

    # Get the user's first group if it exists, otherwise set it to None
    user_group = request.user.groups.first()
    user_group_name = user_group.name if user_group else None

    if user_group_name == "admin":
        announcements = Post.objects.filter(Q(tag="Announcement")).filter(date_time__lte=current_datetime).order_by("-date_time")
        regular_posts = Post.objects.filter(Q(tag="Post")).filter(date_time__lte=current_datetime).order_by("-date_time")
    else:
        announcements = Post.objects.filter(Q(tag="Announcement") & (Q(usergroup="admin") | Q(usergroup=user_group_name))).filter(date_time__lte=current_datetime).order_by("-date_time")
        regular_posts = Post.objects.filter(Q(tag="Post") & (Q(usergroup="admin") | Q(usergroup=user_group_name))).filter(date_time__lte=current_datetime).order_by("-date_time")

    paginator_announcements = Paginator(announcements, 10)
    paginator_regular_posts = Paginator(regular_posts, 10)

    try:
        announcements = paginator_announcements.page(page)
    except PageNotAnInteger:
        announcements = paginator_announcements.page(1)
    except EmptyPage:
        announcements = paginator_announcements.page(paginator_announcements.num_pages)

    try:
        regular_posts = paginator_regular_posts.page(page)
    except PageNotAnInteger:
        regular_posts = paginator_regular_posts.page(1)
    except EmptyPage:
        regular_posts = paginator_regular_posts.page(paginator_regular_posts.num_pages)

    forums = {
        "announcements": announcements,
        "regular_posts": regular_posts,
    }

    return render(request, "home.html", forums)


class PostDetail(DetailView):
    """View Post view"""

    model = Post
    template_name = "forum/post.html"
    slug_field = "slug"
    count_hit = True
    comment_form = NewCommentForm()

    def get_context_data(self, *args, **kwargs):
        """View post (GET) request is called"""
        post_comments_count = (
            Comment.objects.all().filter(post=self.object.id).count()
        )
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(*args, **kwargs)
        context['upload'] = Image.objects.filter(post=self.object)
        context['UploadPDF'] = UploadPDF.objects.filter(post=self.object)
        context.update(
            {
                'post': self.object,
                'post_comments': post_comments,
                'post_comments_count': post_comments_count,
            }
        )
        context["form"] = self.comment_form

        return context

    def post(self, request, *args, **kwargs):
        """Comment POST request is called"""
        username = request.user.username
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            comment_form.instance.name = username
            post = self.get_object()
            user_comment.post = post
            user_comment.save()

            return redirect(request.path_info)
