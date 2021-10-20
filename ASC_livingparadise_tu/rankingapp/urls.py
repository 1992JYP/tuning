
from django.urls.conf import path
from rankingapp.views import ranking_list

app_name ="rankingapp"

urlpatterns = [
   
  
    path('list/', ranking_list, name='list' ),


]
