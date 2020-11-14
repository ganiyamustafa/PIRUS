from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

class LoginUser(LoginView):
    def get_success_url(self):
        return '/'

class LogoutUser(LogoutView):
    def get_success_url(self):
        return '/'
