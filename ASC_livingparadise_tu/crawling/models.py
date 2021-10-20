## 작성 2021-06-17  - 이유인 
## 수정  2021- 07-09  - 이유인

from django.db import models

# Create your models here.
# index_num,item_name, link,pid, price,review_count,image_path,vendor_itemId


# 여기가 models.py에서 설계한 모델을 가져오는 코드입니다






    
    # is_public = models.BooleanField(default=False, verbose_name='공개여부')    공개 여부 
    # photo = models.ImageField(blank=True, upload_to=Crawling/item/%Y%m%d')    사진파일 저장
    #java의 tostring
    # def __str__(self):
    #     # return f'Custom Crawling_item object ({self.item_name})




# 자동 입력 옵션  index/date   
# alter table CP_PRODUCT add DATE_INFO TIMESTAMP DEFAULT NOW(); 

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





class ProductState(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pd_manager = models.CharField(db_column='PD_MANAGER', max_length=30)  # Field name made lowercase.
    pd_code = models.CharField(db_column='PD_CODE', max_length=30)  # Field name made lowercase.
    pd_name = models.CharField(db_column='PD_NAME', max_length=50)  # Field name made lowercase.
    pd_state = models.CharField(db_column='PD_STATE', max_length=20)  # Field name made lowercase.
    pd_review_count = models.IntegerField(db_column='PD_REVIEW_COUNT')  # Field name made lowercase.
    pd_price = models.IntegerField(db_column='PD_PRICE')  # Field name made lowercase.
    pd_grade = models.CharField(db_column='PD_GRADE', max_length=5)  # Field name made lowercase.
    pd_image = models.CharField(db_column='PD_IMAGE', max_length=5000)  # Field name made lowercase.
    pd_url = models.CharField(db_column='PD_URL', max_length=5000)  # Field name made lowercase.
    pd_index = models.IntegerField(db_column='PD_INDEX')  # Field name made lowercase.
    mall_name = models.CharField(db_column='MALL_NAME', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_state'


'ghrkdls'

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