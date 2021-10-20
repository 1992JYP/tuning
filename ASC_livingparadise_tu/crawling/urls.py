## 작성 2021-06-17  - 이유인 
## 수정  2021- 06-25  - 이유인

from. import views
from django.urls import include, path

urlpatterns = [
   
    # 아이템 크롤링하기 
    path('crawling/', views.item_crawling, name='item_crawling' ),
    # 기본 서치
    path('', views.item_search, name='item_list' ),
    # 아이템 상세보기 
    path('item_detail/', views.item_detail, name='item_detail' ),

]
