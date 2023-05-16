from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('<str:coin_name>/',views.coin_chart_page,name='coin_chart_page'),
]