from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from apps.main import views
from apps.main.views import ModelCreateView 

urlpatterns = [
    path('', views.login, name='home'),
    path('test/',views.get_post, name='test'),
    path('btntest/', views.responsetest),
    path('dbtest/',views.dbtest, name = 'dbset'),
    path('keyword/',views.keyword, name = 'keyword'),
    path('review/',views.review, name = 'review'),
    path('Dashboard/',views.Dashboard, name = 'Dashboard'),
    path('create/', ModelCreateView.as_view() ,name='create'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

