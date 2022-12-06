from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Role
from ..forms import RoleForm


def manageRoles(request):
    context = {}
    roles = Role.objects.all()
    context["roles"] = roles
    return render(
        request=request, template_name="roles/roles_index.html", context=context
    )


def createRole(request):
    context = {}
    context["button_name"] = "Create Role"
    context["form"] = RoleForm(request.POST or None)
    if request.method == "POST":
        new_role = context["form"]
        if new_role.is_valid():
            new_role.save()
            return redirect("core.manage_roles")
        else:
            messages.error(request, "something went wrong!")
    return render(
        request=request, template_name="roles/roles_create_update.html", context=context
    )


def updateRole(request, pk):
    context = {}
    current_role = Role.objects.get(id=pk)
    context["button_name"] = "Update Role"
    context["form"] = RoleForm(instance=current_role)
    if request.method == "POST":
        updated_role = RoleForm(request.POST, instance=current_role)
        if updated_role.is_valid():
            updated_role.save()
            return redirect("core.manage_roles")
        else:
            messages.error(request, "something went wrong!")
    return render(
        request=request, template_name="roles/roles_create_update.html", context=context
    )


def deleteRole(request, pk):
    current_role = Role.objects.get(id=pk)
    if current_role:
        current_role.delete()
        return redirect("core.manage_roles")
