from django.db import models

# Create your models here.
class ProductMaster(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pd_manager = models.CharField(db_column='PD_MANAGER', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pd_code = models.CharField(db_column='PD_CODE', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pd_name = models.CharField(db_column='PD_NAME', max_length=45, blank=True, null=True)  # Field name made lowercase.
    pd_brand = models.CharField(db_column='PD_BRAND', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pd_keyword = models.CharField(db_column='PD_KEYWORD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    nv_code = models.CharField(db_column='NV_CODE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    nv_url = models.CharField(db_column='NV_URL', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    cp_code = models.CharField(db_column='CP_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cp_url = models.CharField(db_column='CP_URL', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='IMAGE', max_length=4000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_master'