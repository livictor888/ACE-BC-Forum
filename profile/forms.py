from django.forms import ModelForm
from .models import AboutMe
from crispy_forms.helper import FormHelper

# this form is used to create the form for the about me text

class AboutMeForm(ModelForm):

    class Meta:
        model = AboutMe
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
