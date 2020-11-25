from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('RumahSakit/', views.searchRS.as_view(), name='list_RS'),
    path('RumahSakit/add/', login_required(views.rumahsakitCreate.as_view(template_name="rumahsakit/create_form.html"), login_url='/login/'), name='rs_create'),
    re_path(r'^(?P<pk>[\w|\W]+)/RumahSakit/edit/$', login_required(views.rumahsakitUpdate.as_view(template_name="rumahsakit/create_form.html"), login_url='/login/'), name='rs_update'),
    re_path(r'^(?P<pk>[\w|\W]+)/RumahSakit/delete/$', login_required(views.rumahsakitDelete.as_view(template_name="delete_form.html"), login_url='/login/'), name='rs_delete'),
    re_path(r'^RumahSakit/(?P<rs_requested>[\w|\W]+)/$', views.selectRS.as_view()),
]