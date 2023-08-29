from django.db import models
from tinymce import models as tinymce_models


# this model is used to store the about me text of the user
class AboutMe(models.Model):
    # about_me = models.TextField(max_length=1000, blank=True, null=True)
    about_me = tinymce_models.HTMLField(blank=True, default="")

    def __str__(self):
        return self.about_me
