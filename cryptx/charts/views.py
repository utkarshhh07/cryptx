from django.shortcuts import render
from cryptx.decorators import login_required
from coins.models import Coin
from portfolio.models import Portfolio




@login_required
def coin_chart_page(request,coin_name):
    user=request.user
    coin=Coin.objects.get(name=coin_name)
    quantity = Portfolio.get_quantity(user,coin)

    context = {
        'coin':coin,
        'coin_quantity':quantity,
    }

    return render(request,'charts/coin_chart.html',context)


