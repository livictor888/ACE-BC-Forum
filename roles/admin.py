from django.contrib import admin
from .models import Role
from .forms import RoleForm

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    form = RoleForm
