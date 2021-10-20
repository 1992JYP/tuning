from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from apps.main import views
from apps.main.views import ModelCreateView 

urlpatterns = [
    
    path('', include('apps.users.urls')),



    ## 화면 분활
    path('dashboard/',include("dashboardapp.urls"), name='dashboard'),
    path('ranking/',include("rankingapp.urls"), name='ranking'),
    path('review/',include("reviewapp.urls"), name='review'),
    path('trand_Transition/',include("trand_Transitionapp.urls"), name='trand_Transition'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

