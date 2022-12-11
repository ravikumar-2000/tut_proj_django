from django.contrib import admin
from .models import HMST, PMST, RMST


admin.site.register(PMST)
admin.site.register(RMST)
admin.site.register(HMST)