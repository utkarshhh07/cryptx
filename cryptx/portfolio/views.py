from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4

import json

from coins.models import Coin
from portfolio.models import Portfolio
from orders.models import Order
from dashboard.models import Profile
from cryptx.decorators import *
from django.conf import settings
from django.views.generic.base import TemplateView
import stripe

# Create your views here.

@login_required
def portfolio_home(request):
    user  = request.user
    positions = Order.objects.filter(user=user,order_status=Order.PENDING)
    portfolios = Portfolio.objects.filter(user=user)
    portfolio_qs = []

    for portfolio in portfolios:
        portfolio_qs.append({
            'name':portfolio.coin.name,
            'symbol':portfolio.coin.symbol,
            'avg_price':portfolio.avg_price,
            'quantity':portfolio.quantity
        }) 

    context = {
        'portfolio':portfolio_qs,
        'positions':positions
    }    

    return render(request,'portfolio/portfolio.html',context)





def position_home(request):
    user  = request.user
    positions = Order.objects.filter(user=user,order_status=Order.PENDING)

    context = {
        'positions':positions
    }   

    return render(request,'portfolio/positions.html',context)