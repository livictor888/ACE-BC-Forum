from django.urls import path
from . import views
app_name = 'roles'  

urlpatterns = [

    path('roles/<int:role_id>/edit', views.update_role_code, name='update_role_code'),
]
