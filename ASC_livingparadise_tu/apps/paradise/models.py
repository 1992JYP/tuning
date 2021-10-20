from django.db import models
from django.utils import timezone
from django.db.models import IntegerField, Model
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    name = models.CharField(max_length=100,default="test")
    type = models.CharField(max_length=100,default="")
    url = models.CharField(max_length=500,default="")
    body = models.CharField(max_length=10000,default="")
    rank = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    rating = models.FloatField(max_length=6, default=0.0)
    image_file = models.ImageField(max_length=700, upload_to='media', default='default.jpg')
    image_url = models.URLField(max_length=700, default='www.noimage.com')
    # similar_ids=ArrayField(models.IntegerField(), default=list,blank=True)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=100,default="")
    type = models.CharField(max_length=100,default="")
    url = models.CharField(max_length=500,default="")
    body = models.CharField(max_length=10000,default="")
    rank = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    rating = models.FloatField(max_length=6, default=0.0)
    image_file = models.ImageField(max_length=700, upload_to='media', default='default.jpg')
    image_url = models.URLField(max_length=700, default='www.noimage.com')
    # similar_ids=ArrayField(models.IntegerField(), default=list,blank=True)

    def __str__(self):
        return self.name

class Employees(models.Model):
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMPLOYEES'


class Cp_c_Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    pd_index = models.IntegerField(db_column='PD_INDEX')  # Field name made lowercase.
    change_index = models.IntegerField(db_column='CHANGE_INDEX')  # Field name made lowercase.
    company = models.IntegerField(db_column='COMPANY')  # Field name made lowercase.
    pd_code = models.CharField(db_column='PD_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    keyword = models.CharField(db_column='KEYWORD', max_length=50)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=30)  # Field name made lowercase.
    page_link = models.CharField(db_column='PAGE_LINK', max_length=500)  # Field name made lowercase.
    product_id = models.CharField(db_column='PRODUCT_ID', max_length=50)  # Field name made lowercase.
    price = models.IntegerField(db_column='PRICE')  # Field name made lowercase.
    review_count = models.IntegerField(db_column='REVIEW_COUNT')  # Field name made lowercase.
    image_link = models.TextField(db_column='IMAGE_LINK')  # Field name made lowercase.
    item_id = models.CharField(db_column='ITEM_ID', max_length=50)  # Field name made lowercase.
    grade = models.CharField(db_column='GRADE', max_length=5)  # Field name made lowercase.
    date_info = models.CharField(db_column='DATE_INFO', max_length=50)  # Field name made lowercase.

    class Meta:
        ordering = ['-grade']   # 기본 정렬 설정 하기  -가 붙으면 역순
        managed = False
        db_table = 'cp_product'

class Cp_review(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.CharField(db_column='PRODUCT_ID', max_length=50)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=50)  # Field name made lowercase.
    date = models.DateField(db_column='DATE')  # Field name made lowercase.
    grade = models.IntegerField(db_column='GRADE')  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200)  # Field name made lowercase.
    review = models.TextField(db_column='REVIEW')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cp_review'

class NvProduct(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ranking = models.CharField(max_length=10, blank=True, null=True)
    company = models.CharField(max_length=10, blank=True, null=True)
    item_code = models.CharField(max_length=50, blank=True, null=True)
    keyword = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=30, blank=True, null=True)
    review_count = models.CharField(max_length=30, blank=True, null=True)
    brand = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=2000, blank=True, null=True)
    productid = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    img = models.CharField(max_length=500, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    date_info = models.CharField(max_length=50)
    registration_date = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'nv_product'



class NvReview(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    item_code = models.CharField(max_length=50, blank=True, null=True)
    productid = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    item_option = models.CharField(max_length=200, blank=True, null=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)
    user_star = models.CharField(max_length=10, blank=True, null=True)
    review_create_date = models.CharField(max_length=30, blank=True, null=True)
    review_content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nv_review'



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