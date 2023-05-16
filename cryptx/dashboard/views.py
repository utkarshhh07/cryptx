
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4

import json
from dashboard.models import AccountBook
from cryptx.decorators import *
from coins.models import Coin
from orders.coin_price_api import get_coins
from dashboard.models import Profile


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def dashboard(request):
    user = request.user
    name = user.first_name
    params = {
        'name' : name
    }
    return render(request, 'dashboard/dash.html',params)


def isCoinMatching(str1 , str2):
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

@login_required
def live_search(request,*args):

    query = request.GET.get('query')
    query=query.upper()
    all_coins = Coin.objects.all()

    search_qs = []
    for coin in all_coins:
        if isCoinMatching(coin.name,query) or isCoinMatching(query,coin.name):
            search_qs.append(coin.name)

    resp={
        'coins':search_qs,
    }
    response=json.dumps(resp)
    return HttpResponse(response,content_type='application/json')

@login_required
@profile_required
def profile(request):
    user  = request.user
    name = user.first_name
    lname = user.last_name
    email = user.username
    profile = Profile.objects.get(email = email)
    money=round(profile.money,3)
    params = {
        'name' : name,
        'lname' : lname,
        'email' : email,
        'profile' : profile,
        'money':money
    }
    return render(request , 'dashboard/profile.html',params)


@login_required
def resetpassword(request):
    user = request.user
    if request.method == 'POST':
        password = request.POST.get('password',"")
        confirm_password = request.POST.get('confirmpassword',"")

        if(password != confirm_password):
            return redirect('dashboard')

        user.set_password(password)
        print(password)
        user.save()
        user=authenticate(username=user.email,password=password)
        login(request,user)
        return redirect('dashboard')



@login_required
@ajax_required
def search_query(request,*args):
    user=request.user
    query=request.GET.get('query')
    query.upper()

    is_coin = Coin.objects.filter(name=query)

    print(is_coin,query)

    success=0
    if is_coin:
            success=1
    print("succusses : ",success)
    resp={
        'success':success,
    }
    response=json.dumps(resp)
    return HttpResponse(response,content_type='application/json')


@login_required
def account_book(request,*args):
    user = request.user
    account_book_qs = AccountBook.objects.filter(user=user)

    p = Paginator(account_book_qs, 9)
    page_number = request.GET.get('page')

    try:
        account_book = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        account_book = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        account_book = p.page(p.num_pages)

    context = {
        'account_book':account_book,
    }
    
    return render(request,'dashboard/account_book.html',context=context)
