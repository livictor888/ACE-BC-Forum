from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

from .models import Post, Image, Comment, UploadPDF, CommentReply

class CreatePostForm(forms.ModelForm):
    """Create Post form"""

    title = forms.CharField(max_length=255)
    body = forms.Textarea()
    image = forms.ImageField(
        label="Upload an Image",
        widget=forms.ClearableFileInput(),
        required=False,
    )
    pdf = forms.FileField(
        label="Upload a PDF File",
        widget=forms.ClearableFileInput(),
        required=False,
    )
    CHOICES = []
    label_choices = []

    class Meta:
        model = Post
        fields = ["title", "body", 'youtube']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Button("cancel", "Cancel", css_class="btn btn-secondary", onclick="window.history.back()"))
        self.helper.add_input(Submit("submit", "Submit"))
        self.helper.form_tag = False
        self.user = user

        if self.user and self.user.groups.exists():
            user_group_name = self.user.groups.all()[0].name
        else:
            user_group_name = None
        if user_group_name == 'admin' or (self.user and self.user.is_staff):
            self.CHOICES = [('Announcement', 'Announcement'), ('Post', 'Post')]
            self.fields['tag'] = forms.ChoiceField(
                choices=self.CHOICES, widget=forms.RadioSelect
            )
        else:
            self.CHOICES = [('Post', 'Post')]
            self.fields['tag'] = forms.ChoiceField(
                choices=self.CHOICES,
                widget=forms.RadioSelect,
                initial=self.CHOICES[0][0],
            )
        self.label_choices =[('Meeting-Minutes', 'Meeting Minutes'), 
                             ('Discussion', 'Discussion'),
                             ('Resource-Share', 'Resource Share'),
                             ('Other', 'Other')]
        self.fields['label'] = forms.ChoiceField(
                choices=self.label_choices, 
                widget=forms.RadioSelect,
                initial='',
            )


class EditPostForm(forms.ModelForm):
    """Edit Post form"""

    title = forms.CharField(max_length=255)
    body = forms.Textarea()
    image = forms.ImageField(
        label="Upload an Image",
        widget=forms.ClearableFileInput(),
        required=False,
    )
    pdf = forms.FileField(
        label="Upload a PDF File",
        widget=forms.ClearableFileInput(),
        required=False,
    )
    CHOICES = []
    label_choices = []

    class Meta:
        model = Post
        fields = ["title", "body", 'youtube', 'image', 'pdf', 'tag', 'label']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.user = user

        if self.user and self.user.groups.exists():
            user_group_name = self.user.groups.all()[0].name
        else:
            user_group_name = None

        if user_group_name == 'admin' or (self.user and self.user.is_staff):
            self.CHOICES = [('Announcement', 'Announcement'), ('Post', 'Post')]
            self.fields['tag'] = forms.ChoiceField(
                choices=self.CHOICES, widget=forms.RadioSelect
            )
        else:
            self.CHOICES = [('Post', 'Post')]
            self.fields['tag'] = forms.ChoiceField(
                choices=self.CHOICES,
                widget=forms.RadioSelect,
                initial=self.CHOICES[0][0],
            )

        self.label_choices =[('Meeting-Minutes', 'Meeting Minutes'), 
                             ('Discussion', 'Discussion'),
                             ('Resource-Share', 'Resource Share'),
                             ('Other', 'Other')]
        # Use the current instance's label as initial value
        self.fields['label'] = forms.ChoiceField(
            choices=self.label_choices, 
            widget=forms.RadioSelect,
            initial=self.instance.label if self.instance else '',
        )


class NewCommentForm(forms.ModelForm):
    """Create a Comment class for making comments"""

    class Meta:
        model = Comment
        fields = ("body",)
        # Add styling to the form
        widgets = {
            "body": forms.Textarea(attrs={"class": "col-sm-12", "rows": 5})
        }


class NewReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ("body",)
        # Add styling to the form
        widgets = {
            "body": forms.Textarea(attrs={"class": "col-sm-12", "rows": 5})
        }

class RequiredCheckboxSelectMultiple(CheckboxSelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if index == 0 and 'required' not in attrs:
            option['attrs']['required'] = 'required'
        return option


class AdvancedSearchForm(forms.Form):
    search_terms = forms.CharField(widget=forms.Textarea(attrs={'class': 'search-term-input', 'rows': 4}))
    search_categories = forms.MultipleChoiceField(
        label='Search Categories',
        widget=forms.CheckboxSelectMultiple,
        choices=(
            ('title', 'Title'),
            ('body', 'Body'),
            ('comment', 'Comment')
        )
    )
    search_labels = forms.MultipleChoiceField(
        label='Specify Labels',
        widget=forms.CheckboxSelectMultiple,
        choices=(('Meeting-Minutes', 'Meeting Minutes'), 
                             ('Discussion', 'Discussion'),
                             ('Resource-Share', 'Resource Share'),
                             ('Other', 'Other')
        )
    )



class EditCommentForm(forms.ModelForm):
    """Edit a Comment class for editing comments"""

    class Meta:
        model = Comment
        fields = ["body"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Button("cancel", "Cancel", css_class="btn btn-secondary", onclick="window.history.back()"))
        self.helper.add_input(Submit("submit", "Submit"))
        self.helper.form_tag = False
        self.user = user


class EditCommentReplyForm(forms.ModelForm):
    """Edit a CommentReply class for editing comment replies"""

    class Meta:
        model = CommentReply
        fields = ["body"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Button("cancel", "Cancel", css_class="btn btn-secondary", onclick="window.history.back()"))
        self.helper.add_input(Submit("submit", "Submit"))
        self.helper.form_tag = False
        self.user = user


class DeleteImageForm(forms.Form):
    """Form for deleting images"""

    def __init__(self, *args, post=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = []
        if post:
            self.images = Image.objects.filter(post=post)
    
    
class DeletePDFForm(forms.Form):
    """Form for deleting PDFs"""

    def __init__(self, *args, post=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pdfs = []
        if post:
            self.pdfs = UploadPDF.objects.filter(post=post)