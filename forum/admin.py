from django.contrib import admin
from . import models

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """ register post model """
    list_display = ("title", "body")

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Register comment model """
    list_display = ("post", "name", "date_added", "status")
    list_filter = ("status", "date_added")
    search_fields = ("name", "content")