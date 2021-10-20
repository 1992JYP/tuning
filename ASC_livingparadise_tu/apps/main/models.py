from django.conf.urls import url
from django.db import models
from django.urls.base import reverse_lazy
# Create your models here.
from django.views.generic import CreateView
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class Employees(models.Model):
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMPLOYEES'
    
# def queryone(request):
#     print( 1111111)
#     return render(request, loader.get_template('main/dbtest.html'))


class NvProduct(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank_num = models.CharField(db_column='RANK_NUM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    item_code = models.CharField(db_column='ITEM_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    keyword = models.CharField(db_column='KEYWORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='PRICE', blank=True, null=True)  # Field name made lowercase.
    review_count = models.IntegerField(db_column='REVIEW_COUNT', blank=True, null=True)  # Field name made lowercase.
    serial_number = models.CharField(db_column='SERIAL_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prod = models.CharField(db_column='PROD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='LINK', max_length=500, blank=True, null=True)  # Field name made lowercase.
    score_avg = models.CharField(db_column='SCORE_AVG', max_length=5 , blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='IMAGE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    item_states = models.CharField(db_collation='ITEM_STATES', max_length=500, blank=True, null=True)  # Field name made lowercase.
    date_info = models.DateTimeField(db_column='DATE_INFO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NV_PRODUCT'


class NvReview(models.Model):
    # id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    # pd_index = models.IntegerField(db_column='PD_INDEX', blank=True, null=True)  # Field name made lowercase.
    # serial_number = models.CharField(db_column='SERIAL_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # review_text = models.TextField(db_column='REVIEW_TEXT', blank=True, null=True)  # Field name made lowercase.
    # score = models.IntegerField(db_column='SCORE', blank=True, null=True)  # Field name made lowercase.
    # p_option = models.CharField(db_column='P_OPTION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # review_date = models.CharField(db_column='REVIEW_DATE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    product_id = models.CharField(db_column='PRODUCT_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='DATE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    grade = models.IntegerField(db_column='GRADE', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200,blank=True, null=True)  # Field name made lowercase.
    review = models.TextField(db_column='REVIEW', blank=True, null=True)  # Field name made lowercase.
    p_option = models.CharField(db_column='P_OPTION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'NV_REVIEW'




class Reviewdata(models.Model):
    prod_id = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    match = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    company_check = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    grade = models.IntegerField()
    sales = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    writer = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    regist_date = models.DateField()
    review = models.CharField(max_length=4000, db_collation='utf8mb4_unicode_ci')
    prod_name = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    option = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    prop_result = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    emo_result = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    emo_grade = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'ReviewData'


class Totalkeyword(models.Model):
    prod_name = models.CharField(max_length=1000, db_collation='utf8_unicode_ci')
    prod_id = models.CharField(max_length=1000, db_collation='utf8_unicode_ci')
    analysis_date = models.DateField()
    keyword = models.CharField(max_length=1000)
    key_grade = models.FloatField()
    prod_status = models.CharField(max_length=1000, db_collation='utf8_unicode_ci')

    class Meta:
        managed = False
        db_table = 'TotalKeyword'


class Totalresult(models.Model):
    prod_name = models.CharField(max_length=1000)
    prod_id = models.CharField(max_length=1000)
    prod_status = models.IntegerField()
    size = models.IntegerField()
    price = models.IntegerField()
    usability = models.IntegerField()
    material = models.IntegerField()
    design = models.IntegerField()
    one_point = models.IntegerField()
    two_point = models.IntegerField()
    three_point = models.IntegerField()
    four_point = models.IntegerField()
    five_point = models.IntegerField()
    review_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TotalResult'


class Totalsentence(models.Model):
    prod_name = models.CharField(max_length=1000)
    prod_id = models.CharField(max_length=1000)
    analysis_date = models.DateField()
    sentence = models.CharField(max_length=4000)
    prod_status = models.CharField(max_length=1000, db_collation='utf8_unicode_ci')

    class Meta:
        managed = False
        db_table = 'TotalSentence'


class Emokeyword(models.Model):
    prod_name = models.CharField(max_length=1000)
    prod_id = models.CharField(max_length=1000)
    analysis_date = models.DateField()
    keyword = models.CharField(max_length=1000)
    key_grade = models.IntegerField()
    emo = models.IntegerField()
    prod_status = models.CharField(max_length=1000, db_collation='utf8_unicode_ci')

    class Meta:
        managed = False
        db_table = 'EmoKeyword'


class Emosentence(models.Model):
    prod_name = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    prod_id = models.CharField(max_length=1000, db_collation='utf8mb4_unicode_ci')
    analysis_date = models.DateField()
    sentence = models.CharField(max_length=4000)
    emo = models.IntegerField()
    prod_status = models.CharField(max_length=1000, db_collation='utf8_unicode_ci')

    class Meta:
        managed = False
        db_table = 'EmoSentence'