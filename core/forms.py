from django import forms
from .models import *


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "email", "role"]
