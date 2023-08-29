from django.db import models
from django.utils import timezone
from tinymce import models as tinymce_models
from acebc.storage.storage_backends import PrivateMediaStorage
from django.conf import settings

class Post(models.Model):
    """Post model for saving posts"""

    title = models.CharField("Title", max_length=500)
    body = tinymce_models.HTMLField(blank=True, default="", max_length=1000000)
    date_time = models.DateTimeField(default=timezone.now)
    date_added = models.DateTimeField(default=timezone.now)
    youtube = models.CharField(
        "Youtube Share Link", null=True, blank=True, default=None, max_length=255
    )
    tag = models.CharField("Tag", max_length=255)
    username = models.CharField("Username", max_length=255)
    usergroup = models.CharField("Usergroup", max_length=255, default="admin")
    label = models.CharField("Label", max_length=255, default='Other')
    comments_count = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)

    def __str__(self):
        # turns object into string
        return f"Post: {self.title}"


class Image(models.Model):
    """Saving multiple images"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    if settings.USE_S3 != 'FALSE':
        image = models.ImageField(null=True, blank=True, upload_to="images/", storage=PrivateMediaStorage())
    else:
        image = models.ImageField(null=True, blank=True, upload_to="images/")


class UploadPDF(models.Model):
    """Saving multiple PDFs"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    if settings.USE_S3 != 'FALSE':
        upload_pdf = models.FileField(null=True, blank=True, upload_to="documents/", storage=PrivateMediaStorage())
    else:
        upload_pdf = models.FileField(null=True, blank=True, upload_to="documents/")

    def get_short_filename(self):
        # Split the filename by '/'
        split_by_slash = self.upload_pdf.url.split('/')
        # Take the last item (which should be the filename)
        filename = split_by_slash[-1]
        # Split the filename by '_'
        split_by_underscore = filename.split('_')
        # Take all items except the last one and join them with '_'
        shortened_filename = '_'.join(split_by_underscore[:-1])
        # Add the file extension
        shortened_filename += '.pdf'
        return shortened_filename



class Comment(models.Model):
    """Commenting model for commenting posts"""

    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    body = models.TextField(max_length=1000000)
    date_added = models.DateTimeField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ('date_added',)

    def update_date_time(self):
        self.date_time_field = timezone.now()
        self.save()

    def __str__(self):
        """turns comments into string for readability in the admin page"""
        return '%s - %s' % (self.post.title, self.name)

class CommentReply(models.Model):
    """Reply model for replying to comments"""

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(max_length=250)
    body = models.TextField(max_length=1000000)
    date_added = models.DateTimeField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ('date_added',)

    def update_date_time(self):
        self.date_time_field = timezone.now()
        self.save()

    def __str__(self):
        """turns replies into string for readability in the admin page"""
        return '%s - %s' % (self.comment.name, self.name)
