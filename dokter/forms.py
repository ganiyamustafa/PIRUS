from django import forms
from dal import autocomplete
from dokter.models import Doctor

class CreateDokterForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'Nama': forms.TextInput(attrs={'class': 'input-form mb-10', 'id': 'nama', 'placeholder': 'Nama dokter'}),
            'pengalaman': forms.NumberInput(attrs={'class': 'area-form mb-10', 'id': 'pengalaman', 'placeholder': 'xxx (Tahun)'}),
            'image': forms.FileInput(attrs={'class': 'file-upload-field', 'name': 'file-upload-field', 'id': 'file-upload-field'}),
            'pendidikan': forms.TextInput(attrs={'class': 'input-form mb-10', 'id': 'pendidikan', 'placeholder': 'Universitas xxx'}),
            'rumahsakit': autocomplete.ModelSelect2Multiple(attrs={'name':"rumahsakit", 'id':"rumahsakit", 'class':"multiple-form", 'size': '8'}),
            'spesialis': autocomplete.ModelSelect2Multiple(attrs={'name':"spesialis", 'id':"spesialis", 'class':"multiple-form", 'size': '8'}),
            'Jenkel': autocomplete.ModelSelect2(attrs={'class': 'select-form mb-10', 'id': 'Jenkel'}),
            'tgl_lahir': forms.DateInput(attrs={'class': 'input-form mb-10', 'id': 'tgl_lahir', 'placeholder': 'yyyy-mm-dd'}),
        }