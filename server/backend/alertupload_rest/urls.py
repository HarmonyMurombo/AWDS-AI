from . import views
from rest_framework import routers
from django.urls import path
from rest_framework.authtoken import views as rest_framework_views
from django.urls import path, include , re_path

urlpatterns = [
    path('images/', views.post_alert, name='post_alert'), 
    re_path(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),   
]