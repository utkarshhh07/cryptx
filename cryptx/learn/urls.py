from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.learn , name = 'learn'),
    path('crypto_basics/' , views.crypto_basics , name = 'crypto_basics'),
    path('earn_crypto/' , views.earn_crypto , name = 'earn_crypto'),
    path('trade_crypto/' , views.trade_crypto , name = 'trade_crypto'),
    path('use_crypto/' , views.use_crypto , name = 'use_crypto'),
    path('build_crypto/' , views.build_crypto , name = 'build_crypto'),
    path('crypto_basics/1/' , views.crypto_basics_1 , name = 'crypto_basics_1'),
    path('crypto_basics/2/' , views.crypto_basics_2 , name = 'crypto_basics_2'),
    path('crypto_basics/3/' , views.crypto_basics_3 , name = 'crypto_basics_3'),
    path('coins_info/' , views.coins_info , name = 'coins_info')
]