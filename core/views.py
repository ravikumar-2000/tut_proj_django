from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from .models import Role, UserRole
from .forms import RoleForm


@login_required
def index(request):
    context = {}
    return render(request=request, template_name="base.html", context=context)


def manageUsers(request):
    context = {}
    users = User.objects.all()
    context["users"] = users
    return render(
        request=request, template_name="users/users_index.html", context=context
    )


@login_required
def registerUser(request):
    context = {}
    context["roles"] = Role.objects.all()
    context["button_name"] = "Register User"
    if request.method == "POST":
        new_user = UserCreationForm(request.POST)
        if new_user.is_valid() and request.POST.get("user_role") != "-":
            user = User.objects.create_user(
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                password=request.POST.get("password"),
                is_active=True if request.POST.get("is_active") == "on" else False,
                is_staff=True if request.POST.get("is_staff") == "on" else False,
                is_superuser=True
                if request.POST.get("is_superuser") == "on"
                else False,
            )
            user_role = UserRole()
            user_role.user = user
            user_role.role = Role.objects.get(id=request.POST.get("user_role"))
            user_role.save()
            return redirect("core.manage_users")
        else:
            messages.error(request, message="something went wrong!")
            return redirect("core.register_user")
    context["form"] = UserCreationForm()
    return render(
        request=request,
        template_name="users/user_registration_form.html",
        context=context,
    )


def loginUser(request):
    context = {}
    if request.method == "POST":
        try:
            temp_user = get_object_or_404(User, email=request.POST.get("user_email"))
        except Exception as e:
            temp_user = None
        if temp_user:
            user = authenticate(
                username=temp_user.username, password=request.POST.get("user_password")
            )
            if user:
                login(request=request, user=user)
                return redirect("core.index")
            else:
                messages.error(request, message="credentials does not match")
                return redirect("core.login_user")
        else:
            messages.error(request, message="email address does not exists")
            return redirect("core.login_user")
    return render(
        request=request, template_name="users/user_login_form.html", context=context
    )


@login_required
def logoutUser(request):
    logout(request)
    return redirect("core.index")


@login_required
def updateUser(request, pk):
    context = {}
    current_user = User.objects.get(id=pk)
    current_user_role = UserRole.objects.get(user=current_user)
    context["user_role"] = current_user_role
    context["roles"] = Role.objects.all()
    context["current_user"] = current_user
    context["button_name"] = "Update User"

    if request.method == "POST" and request.POST.get("user_role") != "-":

        current_user.first_name = request.POST.get("first_name")
        current_user.last_name = request.POST.get("last_name")
        current_user.username = request.POST.get("username")
        current_user.email = request.POST.get("email")
        current_user.is_active = (
            True if request.POST.get("is_active") == "on" else False
        )
        current_user.is_staff = True if request.POST.get("is_staff") == "on" else False
        current_user.is_superuser = (
            True if request.POST.get("is_superuser") == "on" else False
        )
        current_user.save()

        current_user_role.role = Role.objects.get(id=request.POST.get("user_role"))
        current_user_role.save()
        return redirect("core.manage_users")
    return render(
        request=request,
        template_name="users/user_registration_form.html",
        context=context,
    )


@login_required
def deleteUser(request, pk):
    current_user = User.objects.get(id=pk)
    if current_user:
        current_user.delete()
        return redirect("core.manage_users")


def manageRoles(request):
    context = {}
    roles = Role.objects.all()
    context["roles"] = roles
    return render(
        request=request, template_name="roles/roles_index.html", context=context
    )


@login_required
def createRole(request):
    context = {}
    context["button_name"] = "Create Role"
    if request.method == "POST":
        new_role = RoleForm(request.POST)
        if new_role.is_valid():
            new_role.save()
            return redirect("core.manage_roles")
        else:
            messages.error(request, "something went wrong!")
            context["form"] = new_role
            return render(
                request=request,
                template_name="roles/roles_create_update.html",
                context=context,
            )
    form = RoleForm()
    context["form"] = form
    return render(
        request=request, template_name="roles/roles_create_update.html", context=context
    )


@login_required
def updateRole(request, pk):
    context = {}
    context["button_name"] = "Update Role"
    current_role = Role.objects.get(id=pk)
    if request.method == "POST":
        updated_role = RoleForm(request.POST, instance=current_role)
        if updated_role.is_valid():
            updated_role.save()
            return redirect("core.manage_roles")
        else:
            messages.error(request, "something went wrong!")
            return render(
                request=request,
                template_name="roles/roles_create_update.html",
                context=context,
            )
    form = RoleForm(instance=current_role)
    context["form"] = form
    return render(
        request=request, template_name="roles/roles_create_update.html", context=context
    )


@login_required
def deleteRole(request, pk):
    current_role = Role.objects.get(id=pk)
    if current_role:
        current_role.delete()
        return redirect("core.manage_roles")


def manageUserRole(request):
    context = {}
    users_roles = UserRole.objects.all()
    context["users_roles"] = users_roles
    return render(
        request=request, template_name="user_role/user_role_index.html", context=context
    )


@login_required
def updateUserRole(request, pk):
    context = {}
    current_user_role = UserRole.objects.get(id=pk)
    context["user_role"] = current_user_role
    context["roles"] = Role.objects.all()
    context["users"] = User.objects.all()
    if request.method == "POST":
        current_user_role.role = Role.objects.get(id=request.POST.get("role_id"))
        current_user_role.save()
        return redirect("core.manage_user_role")
    return render(
        request=request,
        template_name="user_role/user_role_update.html",
        context=context,
    )


@login_required
def deleteUserRole(request, pk):
    user_role = UserRole.objects.get(id=pk)
    if user_role:
        user_role.delete()
        return redirect("core.manage_user_role")


def getPermissions(request):
    context = {}
    users = User.objects.all()
    paginator = Paginator(users, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    context["users"] = page_obj
    return render(
        request=request, template_name="user_permissions/user_permissions_index.html", context=context
    )


def assignPermissions(request):
    context = {}
    query_model = request.GET.get("user_permission_model")
    query_user = request.GET.get('user_id')
    if query_user:
        context['user_id'] = int(query_user)
    if query_model and query_user != '-' and query_model != "-":
        current_user = User.objects.get(id=query_user)
        permissions = Permission.objects.filter(content_type_id=query_model).all()
        context["content_type_id"] = int(query_model)
        context["permissions"] = permissions
    if request.method == "POST":
        for permission in permissions:
            active = int(request.POST.get(permission.codename))
            if current_user.has_perm(permission.content_type.app_label + '.' + permission.codename):
                if active:
                    continue
                else:
                    current_user.user_permissions.remove(permission)
            else:
                if active:
                    current_user.user_permissions.add(permission)
        return redirect("core.get_permissions")
    context['users'] = User.objects.all()
    context["content_types"] = ContentType.objects.all()
    return render(
        request=request,
        template_name="user_permissions/user_assign_permissions.html",
        context=context,
    )


def updatePermissions(request, pk):
    current_user = User.objects.get(id=pk)
    return redirect(f'/user-assign-permissions/?user_id={current_user.id}')


def deletePermissions(request, pk):
    current_user = User.objects.get(id=pk)
    permissions = Permission.objects.filter(user=current_user).all()
    for permission in permissions:
        current_user.user_permissions.remove(permission)
    return redirect('core.get_permissions')