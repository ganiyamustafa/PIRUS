from django.contrib import admin
from rumahsakit.models import Poliklinik, Fasilitas, Daerah, RumahSakit

@admin.register(RumahSakit)
class RSAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Deskripsi Rumah Sakit', {'fields': ('nama', 'alamat', 'no_telp', 'deskripsi','image',)}),
        ('Poliklinik', {'fields': ('poliklinik',)}),
        ('Fasilitas', {'fields': ('fasilitas',)}),
        ('Daerah', {'fields': ('daerah',)}),
    )
    ordering = ('nama', 'daerah',)
    list_filter = ('daerah', 'poliklinik')
    search_fields = ('nama', 'poliklinik')

admin.site.register(Poliklinik)
admin.site.register(Fasilitas)
admin.site.register(Daerah)

