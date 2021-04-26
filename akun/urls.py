from django.contrib.auth import views
from .forms import UserLoginForm
from .views import LoginUser, LogoutUser
from django.urls import path

urlpatterns = [
    path('login/', LoginUser.as_view(template_name="akun/login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutUser.as_view(template_name="index.html"), name='logout'),
]

