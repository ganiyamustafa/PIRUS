from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.searchRS.as_view(), name='rumahsakit'),
    path('add/', login_required(views.rumahsakitCreate.as_view(template_name="rumahsakit/create_form.html"), login_url='/login/'), name='rs_create'),
    path('<pk>/', include([
        path('edit/', login_required(views.rumahsakitUpdate.as_view(template_name="rumahsakit/create_form.html"), login_url='/login/'), name='rs_update'),
        path('delete/', login_required(views.rumahsakitDelete.as_view(template_name="delete_form.html"), login_url='/login/'), name='rs_delete')
    ])),
    path('<rs_requested>/', include([
        path('dokter/', views.rumahsakit_dokter.as_view(), name='rs_dokter'),
        path('', views.selectRS.as_view(), name='rs_selected')
    ])),
]