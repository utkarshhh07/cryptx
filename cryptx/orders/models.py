from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from coins.models import Coin
from dashboard.models import Profile
from portfolio.models import Portfolio
from orders.coin_price_api import get_coin_price

User=get_user_model()


class Order(models.Model):

    BUY,SELL = 1,2
    MODES = (
        (BUY, "Buy"),
        (SELL, "Sell"),
    )

    MARKET,LIMIT,STOPMARKET,STOPLIMIT = 1,2,3,4
    TYPES = (
        (MARKET,'MARKET'),
        (LIMIT,'LIMIT'),
        (STOPMARKET,'STOPMARKET'),
        (STOPLIMIT,'STOPLIMIT'),

    )
    
    PENDING,EXECUTED,CANCELLED,RUNNING = 1,2,3,4
    STATUS = (
        (PENDING,'PENDING'),
        (EXECUTED,'EXECUTED'),
        (CANCELLED,'CANCELLED'),
        (RUNNING,'RUNNING')
    )

    user = models.ForeignKey(User , on_delete = models.CASCADE)
    quantity = models.FloatField(default=0)
    coin = models.ForeignKey(Coin,on_delete=models.CASCADE)
    order_price = models.FloatField(default=0)
    order_type = models.PositiveSmallIntegerField(verbose_name="Type",choices=TYPES,default=1)
    order_status = models.PositiveSmallIntegerField(verbose_name="Status",choices=STATUS,default=1)
    placed_time = models.DateTimeField(default=timezone.now)
    executed_time = models.DateTimeField(default=timezone.now)
    mode = models.PositiveSmallIntegerField(verbose_name="Mode", choices=MODES,default=1)


    class Meta:
        ordering=['-placed_time']

    @classmethod
    def can_be_executed(cls,order_obj):
        # return True
        quantity = order_obj['quantity']
        
        if quantity == 0 :
            return False,"Empty Order is not Allowed"

        user=order_obj['user']
        coin_symbol = order_obj['coin_symbol']
        mode = order_obj['mode']
        order_type = order_obj['order_type']
        limit_price = order_obj['limit_price']
        
        cur_user = Profile.objects.get(email=user.email)
        cur_coin_price = get_coin_price(coin_symbol)
        coin_obj = Coin.objects.get(symbol=coin_symbol)
        total_price = cur_coin_price*quantity

        mode_message = {
            1:'Bought',
            2:'Sold'
        }
        account_message = f'{mode_message[mode]} {quantity} {coin_symbol}'
        if order_type is Order.LIMIT:
            total_price = limit_price*quantity

        print("Money Required: "+str(total_price))


        order_status=cls.EXECUTED
        if order_type==cls.LIMIT:
            order_status = cls.PENDING

        if mode is cls.BUY:
            user_money = cur_user.money

            if total_price>user_money:
                print("Not Enough Balance")
                return False ,"Not Enough Balance , only sufficient for "+str(round(user_money/cur_coin_price,5)) + " "+ coin_symbol
            else:
                 
                if order_type==cls.MARKET:
                    cur_user.deduct_money(user=user,amount=total_price,msg=account_message)
                    # Add coin to portfolio
                    Portfolio.buy_coin(user,quantity,cur_coin_price,coin_obj)

                    # Save new order in DB
                    new_order = Order(
                        user=user,quantity=quantity,coin=coin_obj,
                        order_price=cur_coin_price,mode=mode,
                        order_status = cls.EXECUTED,
                        order_type = cls.MARKET
                    )
                    new_order.save()

                elif order_type==cls.LIMIT:
                    cur_user.deduct_money(user=user,amount=total_price,msg='Blocked for Limit')
                     # Save new order in DB
                    new_order = Order(
                        user=user,quantity=quantity,coin=coin_obj,
                        order_price=limit_price,mode=mode,
                        order_status = cls.PENDING,
                        order_type = cls.LIMIT
                    )
                    new_order.save()
                    

        if mode is cls.SELL:
            user_money = cur_user.money
            coin_quantity = Portfolio.get_quantity(user=user,coin=coin_obj)
            if coin_quantity < quantity: 
                print(f"Not Enough {coin_quantity}")
                return False ,f'Not enough {coin_symbol} only {coin_quantity} are available.' 
            else:   
                Portfolio.sell_coin(user,quantity,cur_coin_price,coin_obj)
                if order_type==cls.MARKET:
                    
                    # add money to user
                    total_price =quantity*cur_coin_price
                    cur_user.add_money(user=user,amount=total_price,msg=account_message)

                    # check if quantity becomes zero after selling
                    Portfolio.check_delete(user,coin_obj)

                    # Save new order in DB
                    new_order = Order(
                        user=user,quantity=quantity,coin=coin_obj,
                        order_price=cur_coin_price,mode=mode,
                        order_status = cls.EXECUTED,
                        order_type = cls.MARKET
                    )
                    new_order.save()

                elif order_type==cls.LIMIT:
                     # Save new order in DB

                    new_order = Order(
                        user=user,quantity=quantity,coin=coin_obj,
                        order_price=limit_price,mode=mode,
                        order_status = cls.PENDING,
                        order_type = cls.LIMIT
                    )
                    new_order.save()


        return True,new_order.id


    @classmethod
    def cancel_order(cls,id,user):
        order = cls.objects.get(id=id)
        mode = order.mode
        if order.order_status != cls.PENDING:
            return False,'Order already Executed'
        order.order_status = cls.CANCELLED
        order.save()

        if mode==cls.BUY:
            # give money back
            profile = Profile.objects.get(email=user.email)
            amount = (order.quantity*order.order_price)
            Profile.add_money(user=user,amount=amount,msg=f'Money Refunded for order id:{id}')

        else:
            # give quantity back
            Portfolio.add_quantity(user,order.coin,order.quantity)

    @classmethod
    def update_order(cls,user,order_id,price,quantity):
        if price <=0 or quantity<=0:
            return False,'price or quantity invalid'
        order = cls.objects.filter(user=user,id=order_id)
        profile = Profile.objects.get(email=user.email)


        if len(order) and order[0].order_status==Order.PENDING:

            order = order[0]
            total_quantity = Portfolio.get_quantity(user,order.coin)
            amount= round(price*quantity,5)
            total_money = profile.money
            money_expended = round(order.quantity*order.order_price,5)
            amount_needed =  amount-money_expended 

            if order.mode == Order.BUY:

                if total_money <amount_needed:
                    return False,f'Not Enough Money'
                else:
                    order.order_price = price
                    order.quantity = quantity
                    order.save()
                    if amount_needed > 0:
                        Profile.deduct_money(user=user,amount=amount_needed,msg=f'Money deducted for update order:{order_id}')
                    elif amount_needed <0:
                        Profile.add_money(user=user,amount=-amount_needed,msg=f'Money refunded for update order:{order_id}')
                    return True,'Order Update Successful'

            if order.mode == Order.SELL:
                quantity_needed = quantity - order.quantity

                if total_quantity < quantity_needed:
                    return False ,f'Not enough {order.coin.symbol} only {total_quantity} more are available.' 
                else:
                    order.order_price = price
                    order.quantity = quantity
                    order.save()
                    if quantity_needed>0:
                        Portfolio.sell_coin(user=user,quantity=-quantity_needed,coin=order.coin)
                    elif quantity_needed<0:
                        Portfolio.add_quantity(user,order.coin,-quantity_needed)
                    return True,'Order Update Successful'

            return False,'Error occured'
        
    def __str__(self):
        return f'{self.user.email} , order id: {self.id} , coin: {self.coin.name}'
    
    def save(self,*args,**kwargs):
        self.order_price = round(self.order_price,5)
        self.quantity = round(self.quantity,5)
        self.executed_time = timezone.now()
        super(Order,self).save(*args,**kwargs)