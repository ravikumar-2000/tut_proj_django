from django.shortcuts import render, HttpResponse
from django_tables2 import SingleTableView
from django_tables2.export.export import TableExport
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django.db.models import Q
import pandas as pd
import numpy as np
from .models import HMST, RMST
from .tables import HmstTable, RmstTable
from .forms import FilterForm


@login_required
def index(request):
    return HttpResponse("hello tanks are here to celebrate!")


@login_required
def exportDataToPdf(request, data_df=None):
    template_path = "components/common_table_data.html"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="report.pdf"'
    # response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    context = {"data": data_df.to_html()}
    template = get_template(template_path)
    html = template.render(context, request)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


@login_required
@permission_required("tank_status.view_hmst", raise_exception=True)
def getHMST(request):
    table = None
    form = FilterForm(request.GET or None)

    if request.GET.get("date_time_from"):
        hmsts = HMST.objects.filter(
            Q(t_stamp__gte=request.GET.get("date_time_from"))
            & Q(t_stamp__lte=request.GET.get("date_time_to")),
        )
        if len(hmsts) > 0:
            table = HmstTable(hmsts)
            table.paginate(page=request.GET.get("page", 1), per_page=15)
            export_format = request.GET.get("_export", None)

            if export_format == "pdf":
                hmsts_df = pd.DataFrame(hmsts.values())
                hmsts_df.index = np.arange(1, len(hmsts_df) + 1)

                # selection of columns
                hmsts_df = hmsts_df.loc[
                    :,
                    [
                        "t_stamp",
                        "hmst_1_status",
                        "hmst_1_quantity",
                        "hmst_1_temp",
                        "hmst_2_status",
                        "hmst_2_quantity",
                        "hmst_2_temp",
                        "hmst_3_status",
                        "hmst_3_quantity",
                        "hmst_3_temp",
                        "hmst_4_status",
                        "hmst_4_quantity",
                        "hmst_4_temp",
                    ],
                ]

                # modification of column
                hmsts_df["t_stamp"] = hmsts_df["t_stamp"].apply(
                    lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
                )

                # modification of column names
                hmsts_df.rename(
                    columns={
                        "t_stamp": "TimeStamp",
                        "hmst_1_status": "HMST 1 Status",
                        "hmst_1_quantity": "HMST 1 Quant",
                        "hmst_1_temp": "HMST 1 Temp",
                        "hmst_2_status": "HMST 2 Status",
                        "hmst_2_quantity": "HMST 2 Quant",
                        "hmst_2_temp": "HMST 2 Temp",
                        "hmst_3_status": "HMST 3 Status",
                        "hmst_3_quantity": "HMST 3 Quant",
                        "hmst_3_temp": "HMST 3 Temp",
                        "hmst_4_status": "HMST 4 Status",
                        "hmst_4_quantity": "HMST 4 Quant",
                        "hmst_4_temp": "HMST 4 Temp",
                    },
                    inplace=True,
                )

                return exportDataToPdf(request, hmsts_df)
            elif TableExport.is_valid_format(export_format):
                exporter = TableExport(export_format, table)
                return exporter.response("table.{}".format(export_format))

    context = {
        "table": table,
        "form": form,
        "form_method": "GET",
        "button_name": "Filter Data",
    }
    return render(request=request, template_name="common_table.html", context=context)


@login_required
@permission_required("tank_status.view_rmst", raise_exception=True)
def getRMST(request):
    table = None
    form = FilterForm(request.GET or None)

    if request.GET.get("date_time_from"):
        rmsts = RMST.objects.filter(
            Q(t_stamp__gte=request.GET.get("date_time_from"))
            & Q(t_stamp__lte=request.GET.get("date_time_to")),
        )
        if len(rmsts) > 0:
            table = RmstTable(rmsts)
            table.paginate(page=request.GET.get("page", 1), per_page=15)
            export_format = request.GET.get("_export", None)

            if export_format == "pdf":
                rmsts_df = pd.DataFrame(rmsts.values())
                rmsts_df.index = np.arange(1, len(rmsts_df) + 1)

                # selection of columns
                rmsts_df = rmsts_df.loc[
                    :,
                    [
                        "t_stamp",
                        "rmst_1_status",
                        "rmst_1_quantity",
                        "rmst_1_temp",
                        "rmst_2_status",
                        "rmst_2_quantity",
                        "rmst_2_temp",
                        "rmst_3_status",
                        "rmst_3_quantity",
                        "rmst_3_temp",
                    ],
                ]

                # modification of column
                rmsts_df["t_stamp"] = rmsts_df["t_stamp"].apply(
                    lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
                )

                # modification of column names
                rmsts_df.rename(
                    columns={
                        "t_stamp": "TimeStamp",
                        "rmst_1_status": "RMST 1 Status",
                        "rmst_1_quantity": "RMST 1 Quant",
                        "rmst_1_temp": "RMST 1 Temp",
                        "rmst_2_status": "RMST 2 Status",
                        "rmst_2_quantity": "RMST 2 Quant",
                        "rmst_2_temp": "RMST 2 Temp",
                        "rmst_3_status": "RMST 3 Status",
                        "rmst_3_quantity": "RMST 3 Quant",
                        "rmst_3_temp": "RMST 3 Temp",
                    },
                    inplace=True,
                )

                return exportDataToPdf(request, rmsts_df)
            elif TableExport.is_valid_format(export_format):
                exporter = TableExport(export_format, table)
                return exporter.response("table.{}".format(export_format))

    context = {
        "table": table,
        "form": form,
        "form_method": "GET",
        "button_name": "Filter Data",
    }
    return render(request=request, template_name="common_table.html", context=context)


# @login_required
# @permission_required("tank_status.view_pmst", raise_exception=True)
# def getPMST(request):
#     return tank_status_controller.getPMSTReport(request)
