from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.portfolio_home,name='portfolio_home'),
    path('positions/',views.position_home,name='position_home')
]