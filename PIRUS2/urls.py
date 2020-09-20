from django.conf import settings
from django.views.static import serve 
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rumahsakit.urls')),
    path('', include('dokter.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]