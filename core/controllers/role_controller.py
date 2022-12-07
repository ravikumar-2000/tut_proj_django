from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Role
from ..forms import RoleForm


def manageRoles(request):

    context = {
        "title": "Manage Roles",
        "roles": Role.objects.all(),
    }

    return render(
        request=request, template_name="roles/roles_index.html", context=context
    )


def createRole(request):

    context = {
        "title": "Create Role",
        "button_name": "Create Role",
        "form": RoleForm(request.POST or None),
    }

    if request.method == "POST":
        new_role = context["form"]
        if new_role.is_valid():
            new_role.save()
            return redirect("core.manage_roles")
        else:
            messages.error(request, "something went wrong!")
    return render(
        request=request, template_name="create_update_form.html", context=context
    )


def updateRole(request, pk):

    current_role = Role.objects.get(id=pk)

    context = {
        "title": f"Update Role {current_role.name}",
        "button_name": "Update Role",
        "form": RoleForm(instance=current_role),
    }

    if request.method == "POST":
        updated_role = RoleForm(request.POST, instance=current_role)
        if updated_role.is_valid():
            updated_role.save()
            return redirect("core.manage_roles")
        else:
            messages.error(request, "something went wrong!")
    return render(
        request=request, template_name="create_update_form.html", context=context
    )


def deleteRole(request, pk):
    current_role = Role.objects.get(id=pk)
    if current_role:
        current_role.delete()
        return redirect("core.manage_roles")
