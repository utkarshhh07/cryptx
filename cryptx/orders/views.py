from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.http import JsonResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4

import json

from coins.models import Coin
from cryptx.decorators import ajax_required
from cryptx.decorators import get_required
from cryptx.decorators import login_required,post_required
from dashboard.models import AccountBook
from portfolio.models import Portfolio
from orders.models import Order
from dashboard.models import Profile

from django.conf import settings
from django.views.generic.base import TemplateView
import stripe

from dashboard.models import Profile, TransactionHistory



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@post_required
def handle_buy(request):
    user=request.user
    coin_symbol = request.POST.get("symbol")
    quantity = float(request.POST.get("quantity"))
    order_type = request.POST.get('order_type')
    limit_price=0

    if(order_type=="LIMIT"):
        limit_price = float(request.POST.get('price'))
    

    if order_type=="MARKET":
        order_type=Order.MARKET
    else:
        order_type=Order.LIMIT

    # user,coin_symbol,quantity,mode,order_type
    order_obj = {
        'user':user,
        'coin_symbol':coin_symbol,
        'quantity':quantity,
        'mode':Order.BUY,
        'order_type':order_type,
        'limit_price':limit_price
    }

    is_executable=Order.can_be_executed(order_obj)

    msg = ""
    success=1
    if is_executable[0]==True:
        msg="Order was Placed Successfully"
    else:
        success=0
        msg=is_executable[1]
    
    # Sending response to frontend for scheduling limit order task
    order = {
        'id':is_executable[1],
        'coin_symbol':coin_symbol,
        'order_type':order_type,
        'limit_price':limit_price,
        'order_mode':Order.BUY,
    }

    resp={
        'order':order,
        'msg':msg,
        'success':success
    }
    response=json.dumps(resp)
    return HttpResponse(response,content_type='application/json')




class wallet_view(TemplateView):
    template_name = 'orders/wallet.html'

    def get_context_data(self, **kwargs): # new
        user = self.request.user
        print(user.username)
        history = TransactionHistory.objects.filter(email = user.username)
        # profile = Profile.objects.filter(email = user.username)
        context = super().get_context_data(**kwargs)
        context['money'] = Profile.get_money(user.username)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['history'] = history
        return context

@login_required
@post_required
def charge(request):
    user=request.user
    print(user.email + " is adding money")
    amount = request.POST.get('amount')
    set_amount = int(amount)*100
    # print(amount)
    charge = stripe.Charge.create(
        amount=set_amount,
        currency='INR',
        description='Money added to Wallet',
        source=request.POST['stripeToken']
    )

    user_profile = Profile.objects.get(email=user.email)
    account_message = 'Added Money to Wallet'
    Profile.add_money(user=user,amount=float(amount),msg=account_message)


    history = TransactionHistory(email = user.email , money = float(amount))
    history.save()

    return render(request, 'orders/charge.html')



@login_required
@post_required
def handle_sell(request):
    user=request.user
    coin_symbol = request.POST.get("symbol")
    quantity = float(request.POST.get("quantity"))
    order_type = request.POST.get('order_type')
    limit_price=0    
    msg = ""
    success=1

    if(order_type=="LIMIT"):
        limit_price = float(request.POST.get('price'))
    

    if order_type=="MARKET":
        order_type=Order.MARKET
    else:
        order_type=Order.LIMIT

    # user,coin_symbol,quantity,mode,order_type
    order_obj = {
        'user':user,
        'coin_symbol':coin_symbol,
        'quantity':quantity,
        'mode':Order.SELL,
        'order_type':order_type,
        'limit_price':limit_price
    }

    is_executable=Order.can_be_executed(order_obj)


    if is_executable[0]==True:
        msg="Order was Placed Successfully"
    else:
        success=0
        msg=is_executable[1]
    
    # Sending response to frontend for scheduling limit order task
    order = {
        'id':is_executable[1],
        'coin_symbol':coin_symbol,
        'order_type':order_type,
        'limit_price':limit_price,
        'order_mode':Order.SELL
    }

    resp={
        'order':order,
        'msg':msg,
        'success':success
    }
    response=json.dumps(resp)

    return HttpResponse(response,content_type='application/json')




@login_required
def order_history(request):
    user = request.user
    user_orders = Order.objects.filter(user=user)

    return render(request,'orders/order_history.html',context={'orders':user_orders})




@login_required
@get_required
def handle_limit_orders(request):
    user=request.user
    order_id = request.GET.get('order_id')
    price = float(request.GET.get('price'))
    user_orders = Order.objects.filter(id=order_id)
    profile = Profile.objects.get(email=user.email)

    if len(user_orders):
        order = user_orders[0]

        # If order already executed
        if order.order_status==Order.EXECUTED:
            print("order already executed")
            resp={
            }
            response=json.dumps(resp)
            return HttpResponse(response,content_type='application/json') 


        order.order_status = Order.EXECUTED
        if order.mode == Order.BUY:
            amount =  (float(order.quantity)*float(order.order_price))-(float(price)*float(order.quantity))
            Profile.add_money(user=user,amount=amount,msg='Limit Money refunded')
            order.order_price =  price
            Portfolio.buy_coin(user,order.quantity,price,order.coin)

        if order.mode == Order.SELL:
            amount = order.quantity * price
            msg = f'Sold {order.quantity} {order.coin.symbol}'
            Profile.add_money(user=user,amount=amount,msg=msg)
            order.order_price =  price
            
            # if quantity becomes zero after selling
            Portfolio.check_delete(user,order.coin)


        order.save()
        profile.save()
        
    resp={
        
    }
    response=json.dumps(resp)
    return HttpResponse(response,content_type='application/json') 


@login_required
@ajax_required
def handle_cancel_order(request):
    user=request.user
    order_id = request.GET.get('id')

    Order.cancel_order(order_id,user)

    return JsonResponse({})


@login_required
@ajax_required
def handle_update_order(request):
    user = request.user
    order_id = request.GET.get('id')
    price = float(request.GET.get('price'))
    quantity = float(request.GET.get('quantity'))

    resp = Order.update_order(user,order_id,price,quantity)
    msg = resp[1]
    success = 1
    if resp[0] == False:
        success = 0

    # Final updated order price
    order = Order.objects.get(id=order_id)

    order = {
        'id':order_id,
        'coin_symbol':order.coin.symbol,
        'order_type':order.order_type,
        'limit_price':order.order_price,
        'order_mode':order.mode
    }

    jsony = {
        'success':success,
        'msg':msg,
        'order':order,
        'email':user.email
    }
    # print(jsony)
    
    return JsonResponse(jsony)