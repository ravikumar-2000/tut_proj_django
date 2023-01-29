from django_tables2 import SingleTableView
from django.shortcuts import render, HttpResponse
from .controllers import tank_status_controller
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def index(request):
    return HttpResponse("hello tanks are here to celebrate!")


@login_required
@permission_required("tank_status.view_hmst", raise_exception=True)
def getHMST(request):
    return tank_status_controller.getHMST(request)


@login_required
@permission_required("tank_status.view_rmst", raise_exception=True)
def getRMST(request):
    return tank_status_controller.getRMST(request)


@login_required
@permission_required("tank_status.view_pmst", raise_exception=True)
def getPMST(request):
    return tank_status_controller.getPMST(request)
