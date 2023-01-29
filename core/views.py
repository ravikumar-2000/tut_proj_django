from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from .models import Role
from .forms import RoleForm
from .controllers import user_controller, role_controller, user_permissions_controller


@login_required
def index(request):
    context = {}
    return render(request=request, template_name="base.html", context=context)


@login_required
@permission_required("core.view_user", raise_exception=True)
def manageUsers(request):
    return user_controller.manageUsers(request)


@login_required
@permission_required("core.add_user", raise_exception=True)
def registerUser(request):
    return user_controller.registerUser(request)


def loginUser(request):
    return user_controller.loginUser(request)


@login_required
def logoutUser(request):
    return user_controller.logoutUser(request)


@login_required
@permission_required("core.change_user", raise_exception=True)
def updateUser(request, pk):
    return user_controller.updateUser(request, pk)


@login_required
@permission_required("core.delete_user", raise_exception=True)
def deleteUser(request, pk):
    return user_controller.deleteUser(request, pk)


@login_required
@permission_required("core.view_role", raise_exception=True)
def manageRoles(request):
    return role_controller.manageRoles(request)


@login_required
@permission_required("core.add_role", raise_exception=True)
def createRole(request):
    return role_controller.createRole(request)


@login_required
@permission_required("core.change_role", raise_exception=True)
def updateRole(request, pk):
    return role_controller.updateRole(request, pk)


@login_required
@permission_required("core.delete_role", raise_exception=True)
def deleteRole(request, pk):
    return role_controller.deleteRole(request, pk)


@login_required
@permission_required("auth.view_permission", raise_exception=True)
def managePermissions(request):
    return user_permissions_controller.managePermissions(request)


@login_required
@permission_required("auth.add_permission", raise_exception=True)
def assignPermissions(request):
    return user_permissions_controller.assignPermissions(request)


@login_required
@permission_required("auth.change_permission", raise_exception=True)
def updatePermissions(request, pk):
    return user_permissions_controller.updatePermissions(request, pk)


@login_required
@permission_required("auth.delete_permission", raise_exception=True)
def deletePermissions(request, pk):
    return user_permissions_controller.deletePermissions(request, pk)
