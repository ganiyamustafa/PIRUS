from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('dokter/', views.SearchDokter.as_view(), name='list_dokter'),
    path('dokter/add/', login_required(views.dokterCreate.as_view(template_name="dokter/create_form.html"), login_url='/login/'), name='rs_create'),
    re_path(r'^(?P<pk>[\w|\W]+)/dokter/edit/$', login_required(views.dokterUpdate.as_view(template_name="dokter/create_form.html"), login_url='/login/'), name='rs_update'),
    re_path(r'^(?P<pk>[\w|\W]+)/dokter/delete/$', login_required(views.dokterDelete.as_view(template_name="delete_form.html"), login_url='/login/'), name='rs_delete'),
    re_path(r'^dokter/(?P<dokter_requested>[\w|\W]+)/$', views.selectDokter.as_view()),
]