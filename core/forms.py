from django import forms
from .models import *


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"
