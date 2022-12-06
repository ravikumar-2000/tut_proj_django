from django.db import models


class PMST(models.Model):
    t_stamp = models.DateTimeField(null=False, blank=False)
    pmst_1_status_int = models.IntegerField(null=True, blank=True)
    pmst_1_status = models.CharField(max_length=50, null=True, blank=True)
    pmst_1_quantity = models.FloatField(null=True, blank=True)
    pmst_1_temp = models.FloatField(null=True, blank=True)
    pmst_2_status_int = models.IntegerField(null=True, blank=True)
    pmst_2_status = models.CharField(max_length=50, null=True, blank=True)
    pmst_2_quantity = models.FloatField(null=True, blank=True)
    pmst_2_temp = models.FloatField(null=True, blank=True)
    pmst_3_status_int = models.IntegerField(null=True, blank=True)
    pmst_3_status = models.CharField(max_length=50, null=True, blank=True)
    pmst_3_quantity = models.FloatField(null=True, blank=True)
    pmst_3_temp = models.FloatField(null=True, blank=True)
    pmst_4_status_int = models.IntegerField(null=True, blank=True)
    pmst_4_status = models.CharField(max_length=50, null=True, blank=True)
    pmst_4_quantity = models.FloatField(null=True, blank=True)
    pmst_4_temp = models.FloatField(null=True, blank=True)
    pmst_5_status_int = models.IntegerField(null=True, blank=True)
    pmst_5_status = models.CharField(max_length=50, null=True, blank=True)
    pmst_5_quantity = models.FloatField(null=True, blank=True)
    pmst_5_temp = models.FloatField(null=True, blank=True)
    pmst_6_status_int = models.IntegerField(null=True, blank=True)
    pmst_6_status = models.CharField(max_length=50, null=True, blank=True)
    pmst_6_quantity = models.FloatField(null=True, blank=True)
    pmst_6_temp = models.FloatField(null=True, blank=True)


class HMST(models.Model):
    pass


class RMST(models.Model):
    pass
