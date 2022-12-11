from django import forms
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin import widgets


class FilterForm(forms.Form):
    date_time_from = forms.DateField(
        label="Date From",
        initial=timezone.now().date(),
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    date_time_to = forms.DateField(
        label="Date To",
        initial=(timezone.now() + timedelta(days=1)).date(),
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
