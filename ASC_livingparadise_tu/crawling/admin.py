## 작성 2021-06-17  - 이유인 
## 수정  2021- 06-22  - 이유인

from django.contrib import admin
from.models import Cp_c_Product , Cp_review
# Register your models here.



#1번째 등록방법

# admin.site.register(Crawling_item)

# 2번째 등록방법

# class Crawling_itemAdimn(admin.ModelAdmin):
    # pass

# admin.site.register(Crawling_item, Crawling_itemAdmin)





# 3번째 방법
@admin.register(Cp_c_Product)
class Crawling_itemAdmin(admin.ModelAdmin):
    list_display = ['keyword','pd_index','product_id','title','price','grade','date_info']  # 공개여부추가 ,'is_public'  
    list_display_links= ['title']                     # 아이템 네임에 링크검
    list_filter = ['date_info','pd_index','grade']                           # 리스트 필터 생성  날짜를 등록날짜 생성시 날자별로 검색가능
    search_fields = ['product_id','title', 'grade']                    # pid, item_name search 창 생성             

@admin.register(Cp_review)
class Crawling_itemAdmin(admin.ModelAdmin):
    list_display = ['product_id','title']  # 공개여부추가 ,'is_public'  
    list_display_links= ['title']                     # 아이템 네임에 링크검
    list_filter = ['product_id']                           # 리스트 필터 생성  날짜를 등록날짜 생성시 날자별로 검색가능
    search_fields = ['product_id','title']                    # pid, item_name search 창 생성      





# 모델에 photo 필드가 존재할시 ( 이미지 사진)
    # def photo_tag(self,Crawling_item):
    #     if Crawling_item.photo:
    #         return mark_safe(f'<img src="{Crawling_item.photo.url}" style="width:50px;"/>')            
    #     return None


# index_num = models.IntegerField(default=0)
#     item_name = models.CharField(max_length=100,default="")
#     link = models.CharField(max_length=500,default="")
#     pid = models.IntegerField(default=0)
#     price = models.IntegerField(default=0)
#     review_count = models.IntegerField(default=0)
#     image_path =models.URLField(max_length=700, default='www.noimage.com') 
#     vendor_itemID = models.IntegerField(default=0)
#   updated_at = models.DateTimeField(auto_now=True)