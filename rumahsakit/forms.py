from django import forms
from rumahsakit.models import RumahSakit

class CreateRumahSakitForm(forms.ModelForm):

    class Meta:
        model = RumahSakit
        fields = '__all__'
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'input__field mb-10', 'id': 'nama', 'placeholder': 'Rumah Sakit xxx'}),
            'alamat': forms.Textarea(attrs={'class': 'input__field mb-10', 'id': 'alamat', 'placeholder': 'jln xxx no xxx'}),
            'no_telp': forms.TextInput(attrs={'class': 'input__field mb-10', 'id': 'no_telp', 'placeholder': '022xxx'}),
            'deskripsi': forms.Textarea(attrs={'class': 'input__field mb-10', 'id': 'deskripsi', 'placeholder': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'file-upload-field mb-10', 'name': 'file-upload-field', 'id': 'file-upload-field'}),
            'poliklinik': forms.SelectMultiple(attrs={'name':"from_poliklinik", 'id':"poliklinik", 'class':"multiple-form mb-10", 'size': '8'}),
            'fasilitas': forms.SelectMultiple(attrs={'name':"from_fasilitas", 'id':"fasilitas", 'class':"multiple-form mb-10", 'size': '8'}),
            'daerah': forms.Select(attrs={'class': 'select-form mb-10', 'id': 'daerah'}),
        }