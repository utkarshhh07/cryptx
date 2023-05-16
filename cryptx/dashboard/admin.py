from django.contrib import admin

# Register your models here.
from .models import AccountBook, Profile,TransactionHistory

admin.site.register(Profile)
admin.site.register(TransactionHistory)
admin.site.register(AccountBook)
