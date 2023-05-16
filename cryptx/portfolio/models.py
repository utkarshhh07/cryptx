from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models.query_utils import Q
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from coins.models import Coin
from dashboard.models import Profile

User=get_user_model()
# Create your models here.


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    coin = models.ForeignKey(Coin, on_delete=CASCADE)
    quantity = models.FloatField(default=0)
    avg_price = models.FloatField(default=0)


    @classmethod
    def add_quantity(cls,user,coin,quantity):
        obj = Portfolio.objects.get(user=user,coin=coin)
        obj.quantity+=quantity
        obj.save()
    

 

    @classmethod
    def get_quantity(cls,user,coin):
        obj = cls.objects.filter(user=user,coin=coin)
        if len(obj):
            return obj[0].quantity
        return 0

    @classmethod 
    def buy_coin(cls,user,quantity,price,coin):
        
        obj, create = cls.objects.get_or_create(user=user,coin=coin)
        total_prev_price = obj.quantity * obj.avg_price
        total_quantity = obj.quantity + quantity
        total_new_price = price*quantity + total_prev_price
        new_avg_price = total_new_price/total_quantity
        obj.quantity = total_quantity
        obj.avg_price = new_avg_price
        # print(f"quantity bought : {quantity} at price : {price} \n total_quantity : {total_quantity} total_price : {total_new_price} \n")
        
        obj.save()



    @classmethod
    def sell_coin(cls,user,quantity,price,coin):
        obj = cls.objects.get(user=user,coin=coin)
        total_quantity = obj.quantity - quantity
        total_quantity = round(total_quantity,4)
        obj.quantity = total_quantity
        obj.save()

    @classmethod
    def check_delete(cls,user,coin):
        obj = cls.objects.get(user=user,coin=coin)
        if obj.quantity==0:
            obj.delete()

    def __str__(self):
        return f'{self.user.email} {self.coin.name}'
    
    def save(self,*args,**kwargs):
        self.avg_price = round(self.avg_price,5)
        self.quantity = round(self.quantity,5)
        super(Portfolio,self).save(*args,**kwargs)
