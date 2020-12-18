from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.SearchDokter.as_view(), name='dokter'),
    path('add/', login_required(views.dokterCreate.as_view(template_name="dokter/create_form.html"), login_url='/login/'), name='dokter_create'),
    path("<pk>/", include([
        path("edit/", login_required(views.dokterUpdate.as_view(template_name="dokter/create_form.html"), login_url='/login/'), name='dokter_update'),
        path("delete/", login_required(views.dokterDelete.as_view(template_name="delete_form.html"), login_url='/login/'), name='dokter_delete'),
    ])),
    path('<dokter_requested>/', views.selectDokter.as_view(), name='dokter_selected'),
]