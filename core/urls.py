from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='core.index'),
    path('manage-users/', views.manageUsers, name='core.manage_users'),
    path('regitser-user/', views.registerUser, name='core.register_user'),
    path('login-user/', views.loginUser, name='core.login_user'),
    path('logout-user/', views.logoutUser, name='core.logout_user'),
    path('update-user/<str:pk>', views.updateUser, name='core.update_user'),
    path('delete-user/<str:pk>', views.deleteUser, name='core.delete_user'),
    path('manage-roles/', views.manageRoles, name='core.manage_roles'),
    path('create-role/', views.createRole, name='core.create_role'),
    path('update-role/<str:pk>', views.updateRole, name='core.update_role'),
    path('delete-role/<str:pk>', views.deleteRole, name='core.delete_role'),
    path('user-roles/', views.manageUserRole, name='core.manage_user_role'),
    path('update-user-role/<str:pk>', views.updateUserRole, name='core.update_user_role'),
    path('delete-user-role/<str:pk>', views.deleteUserRole, name='core.delete_user_role'),
]
