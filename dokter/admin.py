from django.contrib import admin
from dokter.models import Spesialis, Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Deskripsi Dokter', {'fields': ('Nama', 'Jenkel', 'tgl_lahir', 'pendidikan', 'pengalaman', 'image',)}),
        ('Spesialis', {'fields': ('spesialis',)}),
        ('Rumah Sakit', {'fields': ('rumahsakit',)}),
    )
    ordering = ('Nama', 'spesialis', 'rumahsakit')
    list_filter = ('spesialis', 'rumahsakit')
    search_fields = ('nama',)

admin.site.register(Spesialis)
