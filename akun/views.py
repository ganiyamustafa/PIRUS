from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from akun.models import DirekturRS, Admin
from . import forms

def getUserData(request):
    if request.user.is_authenticated:
        if request.user.role == 'D':
            data = DirekturRS.objects.values('id', 'user', 'no_telp', 'email').filter(user=request.user.id)[0]
            rss = DirekturRS.objects.values('rumahsakit').filter(user=request.user.id)[::1]
            data.update({'rumahsakit' : rss})      
        elif request.user.role == 'A': data = Admin.objects.values('id', 'user', 'no_telp', 'email').filter(user=request.user.id)[0]
    else: data = ''
    return data

class LoginUser(LoginView):
    authentication_form = forms.UserLoginForm
    form_class = forms.UserLoginForm
    def get_success_url(self):
        return '/'

class LogoutUser(LogoutView):
    def get_success_url(self):
        return '/'
