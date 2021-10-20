from django.db import models

# Create your models here.
class CategoriCmk(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.BigIntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(blank=True, null=True)
    coupang_cids = models.CharField(max_length=255, blank=True, null=True)
    first_class_name = models.CharField(max_length=255)
    naver_cids = models.CharField(max_length=255, blank=True, null=True)
    second_class_name = models.CharField(max_length=255, blank=True, null=True)
    glowpick_cids = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categori_cmk'




        
class CmkCtest(models.Model):
    id = models.BigIntegerField(primary_key=True)
    cmk_id = models.CharField(max_length=50, blank=True, null=True)
    second_class_name = models.CharField(max_length=50, blank=True, null=True)
    gp_class = models.CharField(max_length=50, blank=True, null=True)
    productid = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    ranking = models.CharField(max_length=30, blank=True, null=True)
    price = models.CharField(max_length=30, blank=True, null=True)
    grade = models.CharField(max_length=30, blank=True, null=True)
    review_count = models.CharField(max_length=30, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    ingredientlist = models.CharField(max_length=5000, blank=True, null=True)
    detail = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=5000, blank=True, null=True)
    imgpath = models.CharField(max_length=5000, blank=True, null=True)
    date_info = models.CharField(max_length=50, blank=True, null=True)
    registration_date = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cmk_ctest'

class CmkBtest(models.Model):
    id = models.BigIntegerField(primary_key=True)
    cmk_id = models.CharField(max_length=50, blank=True, null=True)
    second_class_name = models.CharField(max_length=50, blank=True, null=True)
    gp_class = models.CharField(max_length=50, blank=True, null=True)
    productid = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    ranking = models.CharField(max_length=30, blank=True, null=True)
    price = models.CharField(max_length=30, blank=True, null=True)
    grade = models.CharField(max_length=30, blank=True, null=True)
    review_count = models.CharField(max_length=30, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    ingredientlist = models.CharField(max_length=5000, blank=True, null=True)
    detail = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=5000, blank=True, null=True)
    imgpath = models.CharField(max_length=5000, blank=True, null=True)
    date_info = models.CharField(max_length=50, blank=True, null=True)
    registration_date = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cmk_btest'

class CmkCrtest(models.Model):
    id = models.BigAutoField(primary_key=True)
    cmk_id = models.CharField(max_length=30, blank=True, null=True)
    productid = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)
    user_age = models.CharField(max_length=30, blank=True, null=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    user_gender = models.CharField(max_length=10, blank=True, null=True)
    user_star = models.CharField(max_length=10, blank=True, null=True)
    review_create_date = models.CharField(max_length=100, blank=True, null=True)
    review_content = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cmk_crtest'



class CmkBrtest(models.Model):
    id = models.BigAutoField(primary_key=True)
    cmk_id = models.CharField(max_length=30, blank=True, null=True)
    productid = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)
    user_age = models.CharField(max_length=30, blank=True, null=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    user_gender = models.CharField(max_length=10, blank=True, null=True)
    user_star = models.CharField(max_length=10, blank=True, null=True)
    review_create_date = models.CharField(max_length=100, blank=True, null=True)
    review_content = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cmk_brtest'




class CmkCpProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    cmk_id = models.CharField(max_length=50, blank=True, null=True)
    second_class_name = models.CharField(max_length=50, blank=True, null=True)
    cp_class = models.CharField(max_length=50, blank=True, null=True)
    productid = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    ranking = models.CharField(max_length=30, blank=True, null=True)
    price = models.CharField(max_length=30, blank=True, null=True)
    grade = models.CharField(max_length=30, blank=True, null=True)
    review_count = models.CharField(max_length=30, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    detail = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=5000, blank=True, null=True)
    imgpath = models.CharField(max_length=5000, blank=True, null=True)
    date_info = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cmk_cp_product'



class CmkCpReview(models.Model):
    id = models.BigAutoField(primary_key=True)
    cmk_id = models.CharField(max_length=30)
    productid = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    user_name = models.CharField(max_length=50)
    review_create_date = models.CharField(max_length=100)
    user_star = models.CharField(max_length=10)
    option = models.CharField(max_length=300)
    review_content = models.TextField()

    class Meta:
        managed = False
        db_table = 'cmk_cp_review'





class CmkNvProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    cmk_catid = models.CharField(max_length=50, blank=True, null=True)
    naver_catid = models.CharField(max_length=50, blank=True, null=True)
    second_class_name = models.CharField(max_length=50, blank=True, null=True)
    nv_class = models.CharField(max_length=50, blank=True, null=True)
    productid = models.CharField(max_length=50, blank=True, null=True)
    prod_name = models.CharField(max_length=300, blank=True, null=True)
    ranking = models.CharField(max_length=30, blank=True, null=True)
    price = models.CharField(max_length=30, blank=True, null=True)
    grade = models.CharField(max_length=30, blank=True, null=True)
    review_count = models.CharField(max_length=30, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    detail = models.CharField(max_length=1000, blank=True, null=True)
    ingredientlist = models.CharField(max_length=5000, blank=True, null=True)
    url = models.CharField(max_length=5000, blank=True, null=True)
    imgpath = models.CharField(max_length=5000, blank=True, null=True)
    date_info = models.CharField(max_length=50, blank=True, null=True)
    registration_date = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cmk_nv_product'

class CmkNvReview(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cmk_catid = models.CharField(max_length=50, blank=True, null=True)
    naver_catid = models.CharField(max_length=50, blank=True, null=True)
    productid = models.CharField(max_length=50, blank=True, null=True)
    prod_name = models.CharField(max_length=200, blank=True, null=True)
    option = models.CharField(max_length=200, blank=True, null=True)
    sales = models.CharField(max_length=200, blank=True, null=True)
    writer = models.CharField(max_length=30, blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    regist_date = models.CharField(max_length=30, blank=True, null=True)
    review = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cmk_nv_review'