
from django.urls.conf import path
from reviewapp.views import review_list

app_name ="reviewapp"

urlpatterns = [
   
  
    path('list/', review_list, name='list' ),


]
