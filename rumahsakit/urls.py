from django.urls import path, re_path
from . import views

urlpatterns = [
    path('RumahSakit/', views.searchRS.as_view(), name='list_RS'),
    re_path(r'^RumahSakit/(?P<rs_requested>[\w|\W]+)/$', views.selectRS.as_view()),
]