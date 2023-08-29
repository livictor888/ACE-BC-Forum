from django.shortcuts import render, get_object_or_404, redirect
from .forms import UpdateRoleCodeForm
from .models import Role

# Create your views here.
def update_role_code(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    if request.method == 'POST':
        form = UpdateRoleCodeForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect("/users/")
    else:
        form = UpdateRoleCodeForm(instance=role)
    return render(request, "registration/update_role_code.html", {'form': form})
