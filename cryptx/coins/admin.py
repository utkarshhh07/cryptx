from django.contrib import admin

# Register your models here.
from coins.models import Coin

admin.site.register(Coin)
