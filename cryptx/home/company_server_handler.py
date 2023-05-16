from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4
from .models import Forgotpassword

from django.conf import settings 
from django.core.mail import send_mail
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

# Models
from dashboard.models import Profile


def company_main_server(request):
    user=request.user
    if user.is_authenticated and user.email==settings.COMPANY_EMAIL:
        return render(request,'admin/admin.html')

    return redirect('home')
