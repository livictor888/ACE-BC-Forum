"""acebc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from pages.views import Homepage
from users.views import signup
from users.views import ResetPasswordView, ChangePasswordView, SubscribeView, UnsubscribeView, CustomLoginView
from django.urls import re_path


urlpatterns = [
    path("admin/", admin.site.urls),

    # login ==================================================
    re_path(r'^(?!login/)', include('django.contrib.auth.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),


    # password reset ==================================================
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path(
        'password-change/', ChangePasswordView.as_view(), name='password_change'
    ),
    # password reset ==================================================
    path("users/", include("users.urls")),
    path("", Homepage),
    path("forum/", include("forum.urls")),
    path("profile/", include("profile.urls")),
    path('roles/', include('roles.urls', namespace='roles')),  # include the users app URLs

    path('signup/', signup, name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # <=== serves static media by providing the path of filesystem to the directory and URL that makes the static media accessble via HTTP 
