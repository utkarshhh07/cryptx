
from datetime import time
from os import stat
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
import pytz

from coins.models import Coin

User=get_user_model()

class Profile(models.Model):
    # user = models.ForeignKey(User , on_delete = models.CASCADE)
    email = models.CharField(max_length=50 , default="")
    money = models.FloatField(default=0)
    referral = models.CharField(max_length=50 , default="")

    @classmethod
    def get_money(cls,email):
        return Profile.objects.get(email=email).money

    @classmethod
    #add_money requires user and amound
    def add_money(cls,user,amount,msg='',status=1,type=1):
        profile = cls.objects.filter(email=user.email)
        if len(profile):
            profile[0].money += amount
            AccountBook.add_log(user=user,amount=amount,message=msg,status=status,type=1)
            profile[0].save()
            return True,'Matching Profile Found added money'
        else:
            return False,'No Matching profile can be found to add money'

    @classmethod
    def deduct_money(cls,user,amount,status=1,msg='',type=2):
        profile = cls.objects.filter(email=user.email)
        if len(profile):
            profile[0].money -= amount
            AccountBook.add_log(user=user,amount=amount,message=msg,status=status,type=2)
            profile[0].save()
            return True,'Matching Profile Found deducted money'
        else:
            return False,'No Matching profile can be found to deducted money'

    def save(self,*args,**kwargs):
        self.money = round(self.money,5)
        super(Profile,self).save(*args,**kwargs)

    def __str__(self):
        return self.email


class TransactionHistory(models.Model):
    email = models.CharField(max_length=50 , default="")
    money = models.FloatField(default=0)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.email


class AccountBook(models.Model):
    SUCCESS,CANCELLED = 1,2
    CREDIT,DEBIT=1,2
    STATUS = (
        (SUCCESS,'SUCCESS'),
        (CANCELLED,'CANCELLED')
    )
    TYPES= (
        (CREDIT,'CREDIT'),
        (DEBIT,'DEBIT')
    )
    user = models.ForeignKey(User,verbose_name='User Account Book',on_delete=CASCADE)
    amount = models.DecimalField(max_digits=15,decimal_places=5)
    message = models.CharField(verbose_name='Account Message',default='',max_length=100)
    status = models.PositiveSmallIntegerField(verbose_name='Account Status',choices=STATUS,default=1)
    type = models.PositiveSmallIntegerField(verbose_name="Account Type", choices=TYPES,default=1)
    # PROBLEM: time is being saved as utc format desired utc + 5:30
    time = models.DateTimeField(default=timezone.now)

    @classmethod
    def add_log(cls,user,amount=0,message='',status=1,type=1):
        account_log = cls.objects.create(user=user,amount=amount,message=message,status=status,type=type)
        account_log.save()
        return True,'Account Book entry updated'

    @classmethod
    def remove_log(cls,accountbook_id):
        account_log = cls.objects.filter(id=accountbook_id)

        if len(account_log)==1:
            account_log[0].delete()
            return True,'Account Entry deleted'

        elif len(account_log):
            return False,'No Account Entry Found'


    def __str__(self):
        return  f'{self.user} {self.message} at {self.time.astimezone(pytz.timezone("Asia/Calcutta"))} was {self.status}'

    class Meta:
        ordering=['-time']