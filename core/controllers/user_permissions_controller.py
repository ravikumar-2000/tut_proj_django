from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from ..models import User


def getPermissions(request):

    users = User.objects.all()
    paginator = Paginator(users, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"title": "Manage Permissions", "users": page_obj}

    return render(
        request=request,
        template_name="user_permissions/user_permissions_index.html",
        context=context,
    )


def assignPermissions(request):
    context = {"title": "Assign Permissions"}
    query_model = request.GET.get("user_permission_model")
    query_user = request.GET.get("user_id")
    if query_user:
        context["user_id"] = int(query_user)
    if query_model and query_user != "-" and query_model != "-":
        current_user = User.objects.get(id=query_user)
        permissions = Permission.objects.filter(content_type_id=query_model).all()
        context["content_type_id"] = int(query_model)
        context["permissions"] = permissions
    if request.method == "POST":
        for permission in permissions:
            active = int(request.POST.get(permission.codename))
            if current_user.has_perm(
                permission.content_type.app_label + "." + permission.codename
            ):
                if active:
                    continue
                else:
                    current_user.user_permissions.remove(permission)
            else:
                if active:
                    current_user.user_permissions.add(permission)
        return redirect("core.get_permissions")
    context["users"] = User.objects.all()
    context["content_types"] = ContentType.objects.all()
    return render(
        request=request,
        template_name="user_permissions/user_assign_permissions.html",
        context=context,
    )


def updatePermissions(request, pk):
    current_user = User.objects.get(id=pk)
    return redirect(f"/user-assign-permissions/?user_id={current_user.id}")


def deletePermissions(request, pk):
    current_user = User.objects.get(id=pk)
    permissions = Permission.objects.filter(user=current_user).all()
    for permission in permissions:
        current_user.user_permissions.remove(permission)
    return redirect("core.get_permissions")
