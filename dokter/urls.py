from django.urls import path, re_path
from . import views

urlpatterns = [
    path('dokter/', views.SearchDokter.as_view(), name='list_dokter'),
    # re_path(r'^dokter/(?P<rs_requested>[\w|\W]+)/$', views.selectRS.as_view()),
]