
from django.urls.conf import path
from rankingapp.views import ranking_list
from trand_Transitionapp.views import trand_Transitionapp_list

app_name ="trand_Transitionapp"

urlpatterns = [
   
  
    path('list/', trand_Transitionapp_list, name='list' ),


]
