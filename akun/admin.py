from django.contrib import admin
from akun.models import CustomUser
from akun.models import Admin, DirekturRS
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomAdmin(UserAdmin):
    list_display = ('username', 'role')
    list_filter = ('role',)
    fieldsets = (
        ('Account Profile', {'fields': ('role', 'username', 'password')}),
        ('Account Status', {'fields': ('is_active',)})
    )
    search_fields = ('username',)
    ordering = ('role',)            
    filter_horizontal = ()

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('nama', 'no_telp', 'email')

    fieldsets = (
        ('Profil Admin', {'fields': ('user', 'nama', 'no_telp', 'email')}),        
    )
    search_fields = ('nama',)
    ordering = ('nama',)

@admin.register(DirekturRS)
class DirekturRSAdmin(admin.ModelAdmin):
    list_display = ('nama', 'no_telp', 'email')

    fieldsets = (
        ('Profil DirekturRS', {'fields': ('user', 'nama', 'no_telp', 'email')}),
        ('Rumah Sakit', {'fields': ('rumahsakit',)}),        
    )
    filter_horizontal = ('rumahsakit',)
    search_fields = ('nama', 'rumahsakit')
    ordering = ('nama',)
