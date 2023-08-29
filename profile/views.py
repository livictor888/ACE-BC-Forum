from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView

from .models import AboutMe
from .forms import AboutMeForm

class ProfilePage(TemplateView):
    template_name = "profile/profile.html"

    # take the about me text of the current user from the database and pass it to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['about_me'] = AboutMe.objects.get(
                id=self.request.user.id
            ).about_me

            return context
        except:
            return context


# this view is called when the user clicks on the edit button
class EditProfile(UpdateView):
    form = AboutMeForm()
    template_name = "profile/edit_profile.html"
    context = {"form": form}

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # if the user has already created an about me text, update it
            if AboutMe.objects.filter(id=request.user.id).exists():
                about_me = AboutMe.objects.get(id=request.user.id)
                about_me.about_me = request.POST['about_me']
                about_me.save()
                return redirect('profile:profile')
            # if the user has not created an about me text, create it
            else:
                about_me = AboutMe.objects.create(
                    id=request.user.id, about_me=request.POST['about_me']
                )
                about_me.save()
                return redirect('profile:profile')

    def get(self, request, *args, **kwargs):
        # if the user has already created an about me text, pass it to the template
        if AboutMe.objects.filter(id=request.user.id).exists():
            about_me = AboutMe.objects.get(id=request.user.id)
            form = AboutMeForm(initial={'about_me': about_me.about_me})
            context = {"form": form}
            return render(request, self.template_name, context)
        # if the user has not created an about me text, pass an empty form to the template
        else:
            return render(request, self.template_name, self.context)
