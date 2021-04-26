from django import forms
from rumahsakit.models import RumahSakit, RegisterRumahSakit, RegisterHUMASRS

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

class RegisterRumahSakitForm(forms.ModelForm):

    class Meta:
        model = RegisterRumahSakit
        fields = 'nama', 'alamat', 'no_telp', 'file_akreditansi'
        widgets = {
            'alamat': forms.TextInput(),
        }

class RegisterHUMASRSForm(forms.ModelForm):

    class Meta:
        model = RegisterHUMASRS
        fields = 'nama', 'email', 'no_telp', 'foto_diri', 'foto_ktp'