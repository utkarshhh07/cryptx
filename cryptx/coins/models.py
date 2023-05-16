from typing import Counter
from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

from orders.coin_price_api import get_coin_price

User=get_user_model()

class Coin(models.Model):
    name = models.CharField(unique=True,max_length=30,default="")
    symbol = models.CharField(max_length=30,default="")

    def __str__(self):
       return f"{self.name}({self.symbol})"
    class Meta:
        verbose_name_plural = "Coin"

    @classmethod
    def add_coin(cls,name,symbol):
        name.upper()
        obj = cls.objects.filter(name=name)
        if len(obj):
            return False,f'{name} is already in database'
        obj = cls.objects.create(name=name,symbol=symbol)
        obj.save()
        return True,f'{name} is added to coin database'

    @classmethod
    def remove_coin(cls,name,symbol):
        obj = cls.objects.filter(symbol=symbol,name=name)
        if obj:
            obj.delete()
            return True,f'{name} is delete from coin database'
        return False,'No Such Coin is Present'

    @classmethod 
    def clean_coin_without_image(cls):
        coin_list = cls.objects.all()
        counter = 0
        print(coin_list)
        for coin in coin_list:
            symbol = coin.symbol
            coin.save()
            
            try:
                f = open(f'dashboard/static/dashboard/img/SVG/{symbol}.svg','r')   
            except:
                coin.delete()
            

    @classmethod
    def get_faulty_coins(cls):
        coin_list = cls.objects.all()
        faulty_coins=[]
        for coins in coin_list:
            isvalid = get_coin_price(coins.symbol)
            if isvalid==-1:
                faulty_coins.append(coins)
            
        print( len(faulty_coins) )
        return faulty_coins


    def save(self, *args,**kwargs):
        self.name = self.name.upper()
        self.symbol = self.symbol.upper()
        super(Coin,self).save(*args,**kwargs)

    class Meta:
        ordering = ['-symbol']