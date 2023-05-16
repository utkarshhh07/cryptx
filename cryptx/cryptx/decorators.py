from django.contrib.auth.models import User
from django.shortcuts import redirect

from dashboard.models import Profile



def login_required(func,redirect_name='signup'):
    
    def checkUser(request,*args,**kwargs):
        if not request.user.is_authenticated:
            print('User is not loged in')
            return redirect(redirect_name)
        value = func(request,*args,**kwargs)
        return value
    

    return checkUser

def profile_required(func):
    
    def checkProfile(request,*args,**kwargs):
        user = request.user
        profile = Profile.objects.filter(email=user.email)
        if len(profile)!=1:
            print('User does not have profile pls complete')
            return redirect('home')

        value = func(request,*args,**kwargs)

        return value

    return checkProfile

def ajax_required(func):
    def checkAjax(request,*args,**kwargs):
       
        if not request.is_ajax():
            return redirect('home')

        value = func(request,*args,**kwargs)

        return value

    return checkAjax

def post_required(func):
    def checkPOST(request,*args,**kwargs):
       
        if request.method!="POST":
            return redirect('home')

        value = func(request,*args,**kwargs)

        return value

    return checkPOST

def get_required(func):
    def checkPOST(request,*args,**kwargs):
       
        if  request.method!="GET":
            return redirect('home')

        value = func(request,*args,**kwargs)

        return value

    return checkPOST