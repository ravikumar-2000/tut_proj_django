from django import forms
from .models import *


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'password', 'is_active', 'is_superuser', 'is_staff',
            'role', 'validity_expiry_date'
        ]
