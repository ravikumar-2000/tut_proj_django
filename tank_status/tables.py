import django_tables2 as tables
from .models import HMST, RMST
import itertools


class HmstTable(tables.Table):
    sr_no = tables.Column(empty_values=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(start=1)

    def render_sr_no(self):
        return next(self.counter)

    class Meta:
        model = HMST
        attrs = {"class": "table table-striped table-dark mt-5"}
        template_name = "django_tables2/bootstrap-responsive.html"
        # fields = (
        #     "t_stamp",
        #     "hmst_1_status",
        #     "hmst_1_quantity",
        #     "hmst_1_temp",
        #     "hmst_2_status",
        #     "hmst_2_quantity",
        #     "hmst_2_temp",
        #     "hmst_3_status",
        #     "hmst_3_quantity",
        #     "hmst_3_temp",
        #     "hmst_4_status",
        #     "hmst_4_quantity",
        #     "hmst_4_temp",
        # )
        exclude = (
            "id",
            "hmst_1_status_int",
            "hmst_2_status_int",
            "hmst_3_status_int",
            "hmst_4_status_int",
        )
        sequence = (
            "sr_no",
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
        )


class RmstTable(tables.Table):
    sr_no = tables.Column(empty_values=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(start=1)

    def render_sr_no(self):
        return next(self.counter)

    class Meta:
        model = RMST
        attrs = {"class": "table table-striped table-dark mt-5"}
        template_name = "django_tables2/bootstrap-responsive.html"
        exclude = (
            "id",
            "rmst_1_status_int",
            "rmst_2_status_int",
            "rmst_3_status_int",
        )
        sequence = (
            "sr_no",
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
        )
