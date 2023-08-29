from django.forms import ModelForm
from django import forms
from .models import User
from roles.models import Role
from django.contrib.auth.models import Group

class CreateUserForm(ModelForm):
    """
        This class helps style the form you see in the manage_users.html, and make inputs required.
        The form works of the django form that gets auto generated
        """
    # HTML fields that will show on the manage_users.html
    password = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        min_length=8)
    # required true by defualt

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True)

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True)

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True)

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True)

    # group_choices = [
    #     ('1', 'admin'),
    #     ('2', 'creator'),
    #     ('3', 'viewer'),
    #     ('4', 'faculty'),
    #     ('5', 'service_provider'),
    #     ('6', 'student')
    # ]
    # groups = forms.ChoiceField(
    #     widget=forms.RadioSelect,
    #     choices=group_choices,
    #     required=True)

    groups = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[],
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].choices = [(group.id, group.name) for group in Group.objects.all()]
    # role_code = forms.CharField(
    #     widget=forms.TextInput(
    #     attrs={"class": "form-control", 'placeholder': ('Role Code')}),
    #     required=True)

    # def clean_role_code(self):
    #     role_code = self.cleaned_data['role_code']
    #     if not Role.objects.filter(code=role_code).exists():
    #         raise forms.ValidationError('Invalid role code')
    #     return role_code
    class Meta:
        model = User
        fields = '__all__'  # pass all fields to User model\


class RegisterUserForm(ModelForm):
    """
        This class helps style the form you see in the signup.html, and make inputs required.
        The form works of the django form that gets auto generated
        """

    # HTML fields that will show on the registration.html
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Password'}),
        min_length=8)

    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Confirm Password'}),
        min_length=8)

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", 'placeholder': ('Email')}),
        required=True)

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': ('First Name')}),
        required=True)

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': ('Last Name')}),
        required=True)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': ('Username')}),
        required=True, )

    # role_code = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': ('Role Code')}),
    #                             required=True, )

    # def clean_role_code(self):
    #     value = self.cleaned_data['role_code']
    #     # Store role codes somewhere else
    #     if value not in ROLE_DICT.keys():
    #         raise forms.ValidationError('Invalid Role Code')
    #     return value

    role_code = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True)

    def clean_role_code(self):
        role_code = self.cleaned_data['role_code']
        if not Role.objects.filter(code=role_code).exists():
            raise forms.ValidationError('Invalid role code')
        return role_code

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password',
            'repeat_password', 'role_code')  # pass all fields to User model\
