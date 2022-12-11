from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="tank_status.index"),
    path("get-hmst/", views.getHMST, name="tank_status.get_hmst"),
    path("get-rmst/", views.getHMST, name="tank_status.get_rmst"),
    path("get-pmst/", views.getHMST, name="tank_status.get_pmst"),
]
