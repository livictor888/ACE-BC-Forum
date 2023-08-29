from django import forms
from .models import Role

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'


class UpdateRoleCodeForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['code']  # only code can be edited