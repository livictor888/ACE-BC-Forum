from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib.auth.views import LoginView


#  OUR CREATED MODULES
from .forms import CreateUserForm
from .forms import RegisterUserForm
from roles.models import Role
# ROLE CODES
# from .roles import ROLE_DICT
# RESET PASSWORD MODULES
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect
from acebc.settings import EMAIL_HOST_USER



class SubscribeView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        email = user.email
        if email:
            user.is_subscribed = True
            user.save()

            # Send welcome email
            subject = "Welcome to COPE Forum"
            message = f"Hello {user.first_name},\n\nWelcome to COPE Forum! We are glad to have you as a subscriber. Stay tuned for updates and news.\n\nBest regards,\nThe COPE Forum team\n https://www.copebc.com/"
            from_email = EMAIL_HOST_USER

            bcc_list = [email]
            email = EmailMessage(subject, message, from_email, bcc=bcc_list)
            email.send()

            referer_url = request.META.get('HTTP_REFERER')
            if referer_url:
                return redirect(referer_url)
        return HttpResponse('ERROR subscribing!')


class UnsubscribeView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        email = user.email
        if email:
            user.is_subscribed = False
            user.save()

            # Send welcome email
            subject = "Unsubscribed from COPE Forum"
            message = f"Hello {user.first_name},\n\nWe are sorry to see you go from COPE Forum. We hope you enjoyed being a part of our community and we appreciate the time you spent with us. If you ever want to rejoin us in the future, you are always welcome to do so.\n\nBest regards,\nThe COPE Forum team\n https://www.copebc.com/"
            from_email = EMAIL_HOST_USER

            bcc_list = [email]
            email = EmailMessage(subject, message, from_email, bcc=bcc_list)
            email.send()

            referer_url = request.META.get('HTTP_REFERER')
            if referer_url:
                return redirect(referer_url)
        return HttpResponse('ERROR unsubscribing!')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Reset password request view is rendered here. However, success_message doesn't seem
    to be showing up upon successful password request
    """

    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy('login')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """
    Password reset view is rendered here. However, success_message doesnt seem to be showing up
    upon successful change in password
    """

    template_name = 'registration/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('login')


def register_user(request):
    """
    Manages requests e.g. GET, POST that come into the users/ url also known as manage_users.html
    Only staff are allowed to create new users manually.
    You can create a new user or view the manage_users.html page.
    GET -> return and show the manage_users.html page.
    POST -> creates a new user and checks if values are correct. After redirect to the same page.
    """
    User = get_user_model()
    groups = Group.objects.all()
    roles = Role.objects.all()

    # CREATE NEW USER
    if request.method == "POST":
        # pass all the user input values to the class
        form = CreateUserForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.email = request.POST['email']
            unhashed_pass = request.POST['password']
            post.password = make_password(unhashed_pass)

            # save the object in the database
            post.save()

            # get group id from request
            group_id = request.POST['groups']

            # get group name from auth_group table
            group_name = Group.objects.get(id=group_id)

            # add user to the group
            my_group = Group.objects.get(name=group_name)
            my_group.user_set.add(post)

            # redirect page back to the mange_users.html page to empty the form
            return redirect("/users/")
    else:
        form = CreateUserForm()

    context = {
        'user_groups': {group.name: list(User.objects.filter(groups__name=group.name)) for group in groups},
        'roles': roles,
        'form': form,
    }

    # return manage_users.html with some html variables/objects (GET)
    context.update({'form': form})
    return render(request, "registration/manage_users.html", context)

def delete_user(request):
    """
    Deletes a user from the database and then refreshes the page.
    """
    User = get_user_model()
    if request.method == 'POST':
        user_email = request.POST.get('user_email')

        try:
            user = User.objects.get(email=user_email)
            user.delete()
        except User.DoesNotExist:
            messages.error(request, 'User not found')
        return redirect('/users/')  # Replace this with the appropriate URL pattern name for the user management page
    else:
        return JsonResponse({'result': 'error', 'message': 'Invalid request method'})



def signup(request):
    """
    This function will display the signup page at the /signup url.
    New users enter a role code corresponding to their role.
    Role codes are defined in user/roles.py
    """
    if request.user.is_authenticated:
        return redirect('/')
    form = RegisterUserForm()

    # User registration
    if request.method == "POST":
        # pass all the user input values to the class
        form = RegisterUserForm(request.POST)
        context = {"form": form}
        # check if the form inputs are valid
        if form.is_valid():
            post = form.save(commit=False)
            unhashed_pass = request.POST['password']
            post.password = make_password(unhashed_pass)
            post.save()

            # get role code from request
            role_code = request.POST['role_code']
            try:
                role = Role.objects.get(code=role_code)
                group_name = role.name
            except Role.DoesNotExist:
                # Handle case when the role code is invalid
                form.add_error('role_code', 'Invalid role code')
                return render(request, "registration/signup.html", context)
            # group_name = ROLE_DICT.get(role_code)


        
            # add user to the group
            my_group = Group.objects.get(name=group_name)
            my_group.user_set.add(post)

            # redirect page to the login page
            return redirect("/")
    else:
        form = RegisterUserForm()

    context = {"form": form}
    return render(request, "registration/signup.html", context)


class CustomLoginView(LoginView):
    """
    Overrides the built in loging view to redirect to the home page if the user is already logged in.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
