from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ..models import Role, User
from ..forms import RoleForm, RegistrationForm, UserUpdateForm


def manageUsers(request):
    context = {}
    users = User.objects.all()
    context["users"] = users
    return render(
        request=request, template_name="users/users_index.html", context=context
    )


def registerUser(request):
    context = {}
    context["roles"] = Role.objects.all()
    context["form"] = RegistrationForm(request.POST or None)
    context["button_name"] = "Register User"
    if request.method == "POST":
        new_user = context["form"]
        if new_user.is_valid():
            user_data = request.POST.dict()
            user = User.objects.create_user(
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                username=user_data.get("username"),
                email=user_data.get("email"),
                password=user_data.get("password"),
                validity_expiry_date=user_data.get("validity_expiry_date"),
                is_active=True if user_data.get("is_active") == "on" else False,
                is_staff=True if user_data.get("is_staff") == "on" else False,
                is_superuser=True if user_data.get("is_superuser") == "on" else False,
                role=Role.objects.get(id=user_data.get("role")),
            )
            return redirect("core.manage_users")
        else:
            messages.error(request, message="something went wrong!")
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


def logoutUser(request):
    logout(request)
    return redirect("core.index")


def updateUser(request, pk):
    context = {}
    current_user = User.objects.get(id=pk)
    context["form"] = UserUpdateForm(instance=current_user)
    context["roles"] = Role.objects.all()
    context["button_name"] = "Update User"
    if request.method == "POST":
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
        current_user.role = Role.objects.get(id=request.POST.get("role"))
        current_user.validity_expiry_date = request.POST.get("validity_expiry_date")
        current_user.save()
        return redirect("core.manage_users")
    return render(
        request=request,
        template_name="users/user_registration_form.html",
        context=context,
    )


def deleteUser(request, pk):
    current_user = User.objects.get(id=pk)
    if current_user:
        current_user.delete()
        return redirect("core.manage_users")
