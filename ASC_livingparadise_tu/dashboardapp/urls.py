
from django.urls.conf import path
from dashboardapp.views import dashboard_list,review_dashboard_list
from dashboardapp.views import Sold_out_nv,grade_nv,ranking_top_five_nv,lowest_price_nv,ranking_up_nv, review_dashboard_list,review_lowest_nv
from dashboardapp.views import Sold_out_cp,grade_cp,ranking_top_five_cp,lowest_price_cp,ranking_up_cp,review_lowest_cp

app_name ="dashboardapp"

urlpatterns = [
   
  
    path('list/', dashboard_list, name='list' ),
    path('review_dashboard/', review_dashboard_list, name='review_dashboard' ),

    ## 네이버 팝업창
    path('Sold_out_nv/', Sold_out_nv, name='Sold_out_nv'),
    path('grade_nv/', grade_nv, name='grade_nv'),
    path('ranking_top_five_nv/', ranking_top_five_nv, name='ranking_top_five_nv'),
    path('lowest_price_nv/', lowest_price_nv, name='lowest_price_nv'),
    path('ranking_up_nv/', ranking_up_nv, name='ranking_up_nv'),
    path('review_lowest_nv/', review_lowest_nv, name='review_lowest_nv'),

    ## 쿠팡
    path('Sold_out_cp/', Sold_out_cp, name='Sold_out_cp'),
    path('grade_nv_cp/', grade_cp, name='grade_cp'),
    path('ranking_top_five_cp/', ranking_top_five_cp, name='ranking_top_five_cp'),
    path('lowest_price_cp/', lowest_price_cp, name='lowest_price_cp'),
    path('ranking_up_cp/', ranking_up_cp, name='ranking_up_cp'),
    path('review_lowest_cp/', review_lowest_cp, name='review_lowest_cp'),


]
