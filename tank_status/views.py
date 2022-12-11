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
from .models import HMST
from .tables import HmstTable
from .forms import FilterForm


@login_required
def index(request):
    return HttpResponse("hello tanks are here to celebrate!")


def exportDataToPdf(request, data_df=None):
    template_path = "common_table_data.html"
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
        table = HmstTable(hmsts)
        table.paginate(page=request.GET.get("page", 1), per_page=15)
        export_format = request.GET.get("_export", None)
        if export_format == "pdf":
            hmsts_df = pd.DataFrame(hmsts.values())
            hmsts_df.index = np.arange(1, len(hmsts_df) + 1)
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
            hmsts_df["t_stamp"] = hmsts_df["t_stamp"].apply(
                lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
            )
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


# @login_required
# @permission_required("tank_status.view_rmst", raise_exception=True)
# def getRMST(request):
#     return tank_status_controller.getRMSTReport(request)


# @login_required
# @permission_required("tank_status.view_pmst", raise_exception=True)
# def getPMST(request):
#     return tank_status_controller.getPMSTReport(request)
