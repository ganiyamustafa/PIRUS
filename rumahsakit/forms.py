from django import forms
from dal import autocomplete
from rumahsakit.models import RumahSakit

class CreateRumahSakitForm(forms.ModelForm):

    class Meta:
        model = RumahSakit
        fields = [
            'nama', 'alamat', 'no_telp', 'deskripsi','image',
            'poliklinik',
            'fasilitas',
            'daerah',
        ]
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'input-form mb-10', 'id': 'nama', 'placeholder': 'Rumah Sakit xxx'}),
            'alamat': forms.Textarea(attrs={'class': 'area-form mb-10', 'id': 'alamat', 'placeholder': 'jln xxx no xxx'}),
            'no_telp': forms.TextInput(attrs={'class': 'input-form mb-10', 'id': 'no_telp', 'placeholder': '022xxx'}),
            'deskripsi': forms.Textarea(attrs={'class': 'area-form mb-10', 'id': 'deskripsi', 'placeholder': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'file-upload-field', 'name': 'file-upload-field', 'id': 'file-upload-field'}),
            'poliklinik': autocomplete.ModelSelect2Multiple(attrs={'name':"from_poliklinik", 'id':"poliklinik", 'class':"multiple-form", 'size': '8'}),
            'fasilitas': autocomplete.ModelSelect2Multiple(attrs={'name':"from_fasilitas", 'id':"fasilitas", 'class':"multiple-form", 'size': '8'}),
            'daerah': autocomplete.ModelSelect2(attrs={'class': 'select-form mb-10', 'id': 'daerah'}),
        }