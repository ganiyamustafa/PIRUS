from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.searchRS.as_view(), name='rumahsakit'),
    path('active/<pk>/', views.rumahsakit_activated.as_view(), name='rs_activated'),
    path('change/<pk>/', views.rumahsakit_changed.as_view(), name='rs_change'),
    path('register/', include([
        path('1/', views.register_rumahsakit_step1.as_view(template_name="rumahsakit/register_rumahsakit/register_rumahsakit_step1.html"), name='register_rs_1'),
        path('2/', views.register_rumahsakit_step2.as_view(template_name="rumahsakit/register_rumahsakit/register_rumahsakit_step2.html"), name='register_rs_2'),
        path('3/', views.register_rumahsakit_step3.as_view(), name='register_rs_3'),
        path('list/', include([                
                path('', login_required(views.register_rumahsakit_lists.as_view(), login_url='/login/'), name='register_rs_list'),
                path('delete/<pk>/', login_required(views.register_rumahsakit_denied.as_view(), login_url='/login/'), name='register_rs_denied'),
                path('accepted/<pk>/', login_required(views.register_rumahsakit_accepted.as_view(), login_url='/login/'), name='register_rs_accepted')
            ])),
    ])),
    path('add/', login_required(views.rumahsakitCreate.as_view(template_name="rumahsakit/create_form.html"), login_url='/login/'), name='rs_create'),
    path('<pk>/', include([
        path('edit/', login_required(views.rumahsakitUpdate.as_view(template_name="rum ahsakit/create_form.html"), login_url='/login/'), name='rs_update'),
        path('delete/', login_required(views.rumahsakitDelete.as_view(template_name="delete_form.html"), login_url='/login/'), name='rs_delete')
    ])),
    path('<rs_requested>/', include([
        path('dokter/', views.rumahsakit_dokter.as_view(), name='rs_dokter'),
        path('', views.selectRS.as_view(), name='rs_selected')
    ])),
]