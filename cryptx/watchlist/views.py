from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4
from django.core import serializers
import json
from django.http import JsonResponse
from stripe import log
from cryptx.decorators import *
from coins.models import Coin
from watchlist.models import WatchList


@login_required
def watchlist(request):
    user=request.user
    watchlist_qs = WatchList.objects.filter(user=user)
    context={
        'watchlists':watchlist_qs
    }
    return render(request , 'watchlist/watchlist.html', context)



@login_required
@post_required
def create_watchlist(request):
    user=request.user
    watchlist = request.POST.get('watchlist')

    new_watchlist = WatchList.objects.create(name=watchlist,user=user)
    new_watchlist.save()

    return redirect('watchlist') 



def see_watchlist(request,watchlist):
    user=request.user
    if user.is_authenticated:
        watchlist_qs = WatchList.objects.filter(name=watchlist,user=user)

        if not watchlist_qs:
            return HttpResponse("No such watchlist")

        watchlist_qs=watchlist_qs[0]
        coins = watchlist_qs.coins.all()
        all_coins = Coin.objects.all()

        coins_qs = []
        for coin in coins:
            coins_qs.append({'name':coin.name,'symbol':coin.symbol})

        context = {
            'all_coins':all_coins,
            'coins_qs':coins_qs,
            'name':watchlist
        }
        return render(request,'watchlist/see_watchlist.html',context)

    return redirect('home')


def add_coin(request,*args):
    user = request.user
    if user.is_authenticated:
        coin = request.GET['coin']
        name = request.GET['name']

        WatchList.addcoin(coin,name,user)
        return JsonResponse({})

    return redirect('home')


def delete_coin(request,*args):
    user = request.user
    if user.is_authenticated:
        coin = request.GET['coin']
        name = request.GET['name']

        WatchList.remove_coin(coin,name,user)
        return JsonResponse({})

    return redirect('home')

def coin_matching(str1 , str2):
    #Filters user based on search
    m = len(str1) 
    n = len(str2) 
      
    j = 0   
    i = 0   
      
    while j<m and i<n: 
        if str1[j] == str2[i]:     
            j = j+1    
        i = i + 1
          
    # If all characters of str1 matched, then j is equal to m 
    return j==m 

def delete_watchlist(request,*args):
    user = request.user
    if user.is_authenticated:

        id = request.GET['id']
        watchlist = WatchList.objects.get(id=id)
        if watchlist.user!=user:
            return JsonResponse({'error':"Not Your Watchlist"})

        watchlist.delete()

        return JsonResponse({})

    return redirect('home')

def search_coins(request,*args):
    user = request.user
    if user.is_authenticated:
        all_coins = Coin.objects.all()
        coin = request.GET.get('coin_name')
        coin = coin.upper()
        
        search_coins = []
        coins_symbol = []

        for coins in all_coins:
            if coin_matching(coins.name,coin) or coin_matching(coin,coins.name):
                search_coins.append(coins.name)
                coins_symbol.append(coins.symbol)



        resp = {
            'coins' : search_coins,
            'coins_symbol' : coins_symbol
        }
        response = json.dumps(resp)
        return HttpResponse(response,content_type='application/json')
    return redirect('home')



def share_watchlist(request,id):
    user = request.user
    if user.is_authenticated and request.is_ajax():
        watchlist = WatchList.objects.filter(id=id)
        msg=""
        if len(watchlist)==0:
            msg="Invalid Link"
        else:
            watchlist=watchlist[0]
            if watchlist.user==user:
                msg="Cannot Import Own Watchlist"
            else:
                name=request.GET.get('name')
                new_watchlist = WatchList(name=name,user=user)
                new_watchlist.save()

                for coin in watchlist.coins.all():
                    new_watchlist.addcoin(coin.name,name,user)
                new_watchlist.save()

                msg="Watchlist Successfully imported"

        return JsonResponse({'msg':msg})

    return redirect('home')
