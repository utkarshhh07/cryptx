from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('live_search/',views.live_search,name='live_search'),
    path('profile/',views.profile,name = 'profile'),
    path('account_book/',views.account_book,name = 'account_book'),
    path('resetpassword/', views.resetpassword , name = 'resetpassword'),
    path('search/',views.search_query,name='search'),
]