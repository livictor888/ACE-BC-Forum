import calendar
import datetime
import requests

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    TemplateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse

from .models import Post, Image, Comment, CommentReply, UploadPDF
from .forms import CreatePostForm, NewCommentForm, AdvancedSearchForm, EditCommentForm, NewReplyForm, EditCommentReplyForm, EditPostForm, DeleteImageForm, DeletePDFForm

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q

from datetime import datetime
import re
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

class EditPost(UpdateView):
    """Edit post view"""

    model = Post
    form_class = EditPostForm
    template_name = "forum/post_edit_view.html"
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super(EditPost, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EditPost, self).get_context_data(**kwargs)
        if self.request.POST:
            context['delete_image_form'] = DeleteImageForm(self.request.POST, 
                                                        prefix='images', 
                                                        post=self.object)
            context['delete_pdf_form'] = DeletePDFForm(self.request.POST, 
                                                    prefix='pdfs', 
                                                    post=self.object)
        else:
            context['delete_image_form'] = DeleteImageForm(prefix='images', 
                                                        post=self.object)
            context['delete_pdf_form'] = DeletePDFForm(prefix='pdfs', 
                                                    post=self.object)
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        delete_image_form = context['delete_image_form']
        delete_pdf_form = context['delete_pdf_form']
        self.object = form.save()

        # delete selected images
        delete_images = self.request.POST.getlist('delete_images')
        for image_id in delete_images:
            try:
                Image.objects.get(id=image_id).delete()
            except ObjectDoesNotExist:
                pass

        # delete selected pdfs
        delete_pdfs = self.request.POST.getlist('delete_pdfs')
        for pdf_id in delete_pdfs:
            try:
                UploadPDF.objects.get(id=pdf_id).delete()
            except ObjectDoesNotExist:
                pass
        return HttpResponseRedirect(self.get_success_url())



    def post(self, request, *args, **kwargs):
        """Edit post (POST) request is called"""

        self.object = self.get_object()  
        form = EditPostForm(
        request.POST, request.FILES, instance=self.object, user=request.user
    )
        
        context = self.get_context_data()
        delete_image_form = context['delete_image_form']
        delete_pdf_form = context['delete_pdf_form']
        files = request.FILES.getlist("image", None)
        pdf_files = request.FILES.getlist("pdf")
        username = request.user.username
        usergroup = request.user.groups.all()[0].name

        if form.is_valid():
            post = form.save(commit=False)
                    # delete selected images
            delete_images = self.request.POST.getlist('delete_images')
            for image_id in delete_images:
                try:
                    Image.objects.get(id=image_id).delete()
                except ObjectDoesNotExist:
                    pass

            # delete selected pdfs
            delete_pdfs = self.request.POST.getlist('delete_pdfs')
            for pdf_id in delete_pdfs:
                try:
                    UploadPDF.objects.get(id=pdf_id).delete()
                except ObjectDoesNotExist:
                    pass
            tag = request.POST['tag']
            yt_url = request.POST['youtube']
            yt_embedded = get_youtube_embedded_url(yt_url)

            # Updating the form to Post model ===========================================
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.tag = tag
            post.youtube = yt_embedded
            post.username = username
            post.usergroup = usergroup
            post.edited = True
            post.date_time = datetime.now()
            post.save()

            # Issue: currently both pdf and image files can only be added not removed when editing the post
            if settings.USE_S3 != 'FALSE':  # Check if we are using S3
                for pdf in pdf_files:
                    pdf_instance = UploadPDF(upload_pdf=pdf, post=post)  # Save to S3
                    pdf_instance.save()
                for file in files:
                    image_instance = Image(image=file, post=post)  # Create a new Image instance and associate it with the post
                    image_instance.save()
            else:
                for file in files:
                    Image.objects.create(post=post, image=file)
                for pdf in pdf_files:
                    UploadPDF.objects.create(post=post, upload_pdf=pdf)
            if 'save_and_continue' in request.POST:
                return HttpResponseRedirect(reverse('forum:editpost', args=[post.id]))
            else:
                return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostList(ListView):
    """Posts view"""
    
    model = Post
    template_name = "forum/posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        """Get query (GET) request is called"""
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        qs = super().get_queryset()
        current_datetime = datetime.now()

        if self.request.user.groups.all()[0].name == "admin":
            regular_posts = qs
        else:
            regular_posts = qs.filter(
                Q(usergroup=self.request.user.groups.all()[0].name) | Q(usergroup="admin")
            )

        if month and year:
            return (
                regular_posts.filter(date_time__year=year)
                .filter(date_time__month=month)
                .order_by("-date_time")
            )
        regular_posts.order_by("-date_time")
        return regular_posts


class Search(ListView):
    """Search view"""
    template_name = "forum/search_results.html"
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self, **kwargs):
        search = self.kwargs["search"].replace("__slash__", "/")

        substrings = search.split()

        filtered_words = substrings

        q_obj_body = Q()
        q_obj_title = Q()

        for substring in filtered_words:
            q_obj_body |= Q(body__icontains=substring)
            q_obj_title |= Q(title__icontains=substring)

        current_datetime = datetime.now()
        if len(filtered_words) > 0:
            combined_qs = Post.objects.filter(q_obj_body | q_obj_title)
            comment_qs = Comment.objects.filter(q_obj_body)
        else:
            combined_qs = Post.objects.none()
            comment_qs = Comment.objects.none()

        # Check if the first group of the current user is 'admin'
        if self.request.user.groups.filter(name="admin").exists():
            # If the user is an admin, we don't apply any additional filters
            combined_qs_excluded = combined_qs
            datesorted_comments = comment_qs
        else:
            combined_qs_excluded = combined_qs.filter(
                Q(usergroup=self.request.user.groups.all()[0].name)
                | Q(tag='Announcement')
                | Q(usergroup="admin")
            )

            # Filtering comments according to user's group
            datesorted_comments = comment_qs.filter(Q(post__usergroup=self.request.user.groups.all()[0].name)| 
                                                    Q(post__usergroup="admin"))
        results = combined_qs_excluded
        combined_results = list(datesorted_comments) + list(results)
        sorted_queryset = sorted(combined_results, key=lambda obj: obj.date_time, reverse=True)

        return sorted_queryset



class MonthList(TemplateView):
    """Date filter (month) view"""

    template_name = "forum/month_list.html"

    def get_context_data(self, **kwargs):
        """Month(GET) request is called"""
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        year = self.kwargs["year"]
        current_datetime = datetime.now()

        # Check if the user has any groups, if not, return an empty queryset
        if not context["request"].user.groups.exists():
            regular_posts = Post.objects.none()
        # If the user is an admin, return all posts
        elif context["request"].user.groups.all()[0].name == "admin":
            regular_posts = Post.objects
        # Otherwise, return only posts related to the user's group
        else:
            regular_posts = Post.objects.filter(
                Q(usergroup=context["request"].user.groups.all()[0].name) | Q(usergroup="admin")
            )

        # Get distinct months for posts in the given year
        months = (
            regular_posts.filter(date_time__year=year)
            .values_list('date_time__month', flat=True)
            .distinct().order_by("-date_time")
        )

        context["year"] = year
        context["months"] = {
            month: calendar.month_name[month] for month in months
        }
        return context


class YearList(TemplateView):
    """Date filter (year) view"""

    template_name = "forum/year_list.html"

    def get_context_data(self, **kwargs):
        """Year(GET) request is called"""
        context = super().get_context_data(**kwargs)
        context["request"] = self.request

        # Check if the user has any groups, if not, return an empty queryset
        if not context["request"].user.groups.exists():
            regular_posts = Post.objects.none()
        # If the user is an admin, return all posts
        elif context["request"].user.groups.all()[0].name == "admin":
            regular_posts = Post.objects
        # Otherwise, return only posts related to the user's group
        else:
            regular_posts = Post.objects.filter(
                Q(usergroup=context["request"].user.groups.all()[0].name) | Q(usergroup="admin")
            )

        years = list(
            set(regular_posts.all().values_list('date_time__year', flat=True))
        )
        years.sort(reverse=True)

        context["years"] = {year: year for year in years}
        return context


class PostDetail(DetailView):
    """View Post view"""

    model = Post
    template_name = "forum/post.html"
    slug_field = "slug"
    count_hit = True
    comment_form = NewCommentForm()

    def get_context_data(self, *args, **kwargs):
        """View post (GET) request is called"""
        
        # Access the Adobe API key from the settings file
        adobe_api_key = settings.ADOBE_API_KEY

        post_comments = Comment.objects.filter(post=self.object.id)
        post_comments_count = post_comments.count()


        # Update the comments_count field in the related Post object
        post = self.get_object()
        # Count the number of comment replies in the post
        comment_replies_count = sum(
            CommentReply.objects.filter(comment=comment.id).count()
            for comment in post_comments
        )
    
        # Update the comments_count field in the related Post object to include replies
        post = self.get_object()
        post.comments_count = post_comments_count + comment_replies_count
        post.save()
        
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(*args, **kwargs)
        context['upload'] = Image.objects.filter(post=self.object)
        context['UploadPDF'] = UploadPDF.objects.filter(post=self.object)
        context.update(
            {
                'post': self.object,
                'post_comments': post_comments,
                'post_comments_count': post_comments_count,
                'comment_replies_count': comment_replies_count,  # Add comment replies count to context
            }
        )
        context["form"] = self.comment_form
        context["reply_form"] = NewReplyForm()  # Add a reply form to the context
        context["adobe_api_key"] = adobe_api_key
        return context
    

    def post(self, request, *args, **kwargs):
        username = request.user.username
        comment_pk = request.POST.get('comment_pk')

        # If 'comment_pk' exists in POST data, handle the reply form
        if comment_pk:
            reply_form = NewReplyForm(request.POST)
            if reply_form.is_valid():
                user_reply = reply_form.save(commit=False)
                reply_form.instance.name = username
                comment = Comment.objects.get(pk=comment_pk)
                user_reply.comment = comment
                user_reply.save()
            return redirect(request.path_info)

        # If 'comment_pk' does not exist, handle the comment form
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            comment_form.instance.name = username
            post = self.get_object()
            user_comment.post = post
            user_comment.save()
            return redirect(request.path_info)

        # If neither form is valid, you can choose to return an error message or just redirect back to the page
        return redirect(request.path_info)


def get_youtube_embedded_url(url):
    """
    Convert any youtube URL into an embedded youtube URL
    """
    if url is not None:
        # Regular expression to extract the video ID
        youtube_regex = (
            r"(https?://)?(www\.)?"
            "(youtube|youtu|youtube-nocookie)\.(com|be)/"
            "(watch\?v=|embed/|v/|.+\/)?([^&=%\?]{11})"
        )

        youtube_regex_match = re.match(youtube_regex, url)
        if youtube_regex_match:
            youtube_id = youtube_regex_match.group(6)
            return f"https://www.youtube.com/embed/{youtube_id}"
    return None



class PostCreate(FormView):
    """Create Post view"""

    model = Post
    form_class = CreatePostForm
    template_name = "forum/create.html"
    success_url = "/"

    def post(self, request, *args, **kwargs):
        """Create post (POST) request is called"""
        form = CreatePostForm(request.POST, request.FILES, user=request.user)
        files = request.FILES.getlist("image")
        pdf_files = request.FILES.getlist("pdf")
        username = request.user.username

        # Check if the user has any groups, if not, set usergroup to None
        if not request.user.groups.exists():
            usergroup = None
        else:
            usergroup = request.user.groups.all()[0].name

        if form.is_valid():
            post = form.save(commit=False)
            tag = request.POST['tag']
            label = request.POST['label']
            yt_url = request.POST['youtube']

            # call the function to get the embedded URL
            yt_embedded = get_youtube_embedded_url(yt_url)

            # Saving the form to Post model ===========================================
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.tag = tag
            post.youtube = yt_embedded
            post.username = username
            post.usergroup = usergroup
            post.label = label
            post.save()

            if settings.USE_S3 != 'FALSE':  # Check if we are using S3
                for pdf in pdf_files:
                    pdf_instance = UploadPDF(upload_pdf=pdf, post=post)
                    pdf_instance.save()
                for file in files:
                    image_instance = Image(image=file, post=post)  # Create a new Image instance and associate it with the post
                    image_instance.save()
            else:
                for file in files:
                    Image.objects.create(post=post, image=file)
                for pdf in pdf_files:
                    UploadPDF.objects.create(post=post, upload_pdf=pdf)
            if 'save_and_continue' in request.POST:
                return HttpResponseRedirect(reverse('forum:editpost', args=[post.id]))
            else:
                return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        """Get form kwargs"""
        kwargs = super(PostCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DeletePost(DeleteView):
    """Delete post view"""

    model = Post
    success_url = "/"
    template_name = "forum/confirm_delete_post.html"


class AdvancedSearch(FormView):
    """ Advanced Search view """
    template_name = 'forum/advanced_search.html'
    form_class = AdvancedSearchForm
    paginate_by = 10  # Number of items to display per page
    success_url = '/forum/advsearch/result/'

    def form_valid(self, form):
        # Get the form data
        search_terms_value = form.cleaned_data['search_terms']
        search_categories_value = form.cleaned_data['search_categories']
        search_labels_value = form.cleaned_data['search_labels']

        # Store form data in session
        self.request.session['search_terms'] = search_terms_value
        self.request.session['search_categories'] = search_categories_value
        self.request.session['search_labels'] = search_labels_value

        return super().form_valid(form)

class AdvSearchResult( ListView ):
    """AdvSearchResult view"""

    template_name = 'forum/search_results.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        search_terms_value = self.request.session.get('search_terms')
        search_categories_value = self.request.session.get('search_categories')
        search_labels_value = self.request.session.get('search_labels')

        response = requests.get(
                'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt'
            )
        frequent_words = response.content.decode('utf-8').splitlines()[
                :25
            ]  # Only keep the top 50 frequent words

        substrings = search_terms_value.split()

        if len(substrings) > 3:
            filtered_words = [
                word for word in substrings if word.lower() not in frequent_words
            ]
        else:
            filtered_words = substrings


        q_obj_body = Q()
        q_obj_title = Q()
        q_obj_comment = Q()

        if "title" in search_categories_value:
            for substring in filtered_words:
                q_obj_title |= Q(title__icontains=substring)

        if "body" in search_categories_value:
            for substring in filtered_words:
                q_obj_body |= Q(body__icontains=substring)

        if "comment" in search_categories_value:
            for substring in filtered_words:
                q_obj_comment |= Q(body__icontains=substring)

        current_datetime = datetime.now()
        if len(filtered_words) > 0:
            if "title" in search_categories_value and "body" in search_categories_value:
                combined_qs = Post.objects.filter(q_obj_body | q_obj_title)
            elif "body" in search_categories_value:
                combined_qs = Post.objects.filter(q_obj_body)
            elif "title" in search_categories_value:
                combined_qs = Post.objects.filter(q_obj_title)
            else:
                combined_qs = Post.objects.none()
            if "comment" in search_categories_value:
                comment_qs = Comment.objects.filter(q_obj_comment)
            else:
                comment_qs = Comment.objects.none()
        else:
            combined_qs = Post.objects.none()

        combined_qs_excluded = combined_qs.filter(
            Q(usergroup=self.request.user.groups.all()[0].name)
            | Q(tag='Announcement')| 
            Q(usergroup="admin")
        )
        posts_sorted = combined_qs_excluded.filter(
            date_time__lte=current_datetime
        ).order_by("-date_time")
        
        results = posts_sorted.filter(label__in=search_labels_value)


        # # PROCESSING COMMENT QUERY
        datesorted_comments = comment_qs.filter(Q(post__usergroup=self.request.user.groups.all()[0].name) | 
                                                    Q(post__usergroup="admin"))
        results_comments = datesorted_comments.filter(post__label__in=search_labels_value)

        combined_results = list(datesorted_comments) + list(results)
        sorted_queryset = sorted(combined_results, key=lambda obj: obj.date_time, reverse=True)
        return sorted_queryset



class EditCommentView(UpdateView):
    """Edit comment view"""
    model = Comment
    form_class = EditCommentForm
    template_name = "forum/edit_comment.html"
    success_url = "/"
    
    pk_url_kwarg = 'comment_pk'

    def form_valid(self, form):
        form.instance.date_time = datetime.now()
        form.instance.edited = True
        return super().form_valid(form)

    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse_lazy('forum:detail', kwargs={'pk': post_pk})

    def get(self, request, *args, **kwargs):
        comment_pk = self.kwargs['comment_pk']
        comment = Comment.objects.get(pk=comment_pk)
        form = EditCommentForm(instance=comment)
        return render(request, 'forum/edit_comment.html', {'form': form, 'is_edit_comment_page': True})


class DeleteComment(DeleteView):
    """Delete comment view"""

    model = Comment
    success_url = "/"
    template_name = "forum/confirm_delete_comment.html"
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse_lazy('forum:detail', kwargs={'pk': post_pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


class EditCommentReplyView(UpdateView):
    """Edit comment reply view"""
    model = CommentReply
    form_class = EditCommentReplyForm
    template_name = "forum/edit_comment_reply.html"
    success_url = "/"

    pk_url_kwarg = 'comment_reply_pk' 
    def form_valid(self, form):
        form.instance.date_time = datetime.now()
        form.instance.edited = True
        return super().form_valid(form)

    def get_success_url(self):
        # Note: CommentReply doesn't have a direct relationship with Post.
        # Here we're getting the post through the Comment related to the CommentReply.
        post_pk = self.object.comment.post.pk
        return reverse_lazy('forum:detail', kwargs={'pk': post_pk})

    def get(self, request, *args, **kwargs):
        comment_reply_pk = self.kwargs['comment_reply_pk']  
        comment_reply = CommentReply.objects.get(pk=comment_reply_pk)  
        form = EditCommentReplyForm(instance=comment_reply)  
        return render(request, 'forum/edit_comment_reply.html', {'form': form, 'is_edit_comment_page': True})


class DeleteCommentReply(DeleteView):
    """Delete comment reply view"""

    model = CommentReply
    success_url = "/"
    template_name = "forum/confirm_delete_comment_reply.html"
    pk_url_kwarg = 'comment_reply_pk' 

    def get_success_url(self):
        post_pk = self.object.comment.post.pk # get the post through the comment
        return reverse_lazy('forum:detail', kwargs={'pk': post_pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
