from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

from . import company_server_handler


urlpatterns = [
    
    path('company_main_server/',company_server_handler.company_main_server,name='company_main_server'),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signuph/',views.signuphandle,name='signuph'),
    path('logout/',views.logout_user,name='logout'),
    path('login/',views.login_page,name='login_page'),
    path('forgotpassword/',views.forgotpassword , name = 'forgotpassword'),
    path('handleforgotpassword/', views.handle_forgotpassword , name = 'handle_forgot_password'),
    path('auth_forgot/<str:token>',views.auth_forgot_password,name="auth_forgot_password"),
    path('resetpassword/<str:token>',views.reset_password,name="reset_password"),
    path('reports/report_generator/',views.report_generator,name='report_generator'),
    path('debug/',views.debug,name='debug')
]