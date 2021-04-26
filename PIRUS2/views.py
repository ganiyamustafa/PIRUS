from django.shortcuts import render, redirect
from django.views.generic import View
from rumahsakit.forms import CreateRumahSakitForm
from rumahsakit.models import RegisterRumahSakit, RegisterHUMASRS, RumahSakit
from akun.models import DirekturRS

class Index(View):
    reg_humas = reg_rs = humas_rs = None
    def get_reg_rs(self, pk):
        self.reg_rs = RegisterRumahSakit.objects.get(id=pk)

    def get_reg_humas(self, request):
        self.humas_rs = DirekturRS.objects.values('nama', 'rumahsakit').filter(user=request.user.id)[0]
        try: self.reg_humas = RegisterHUMASRS.objects.get(nama=self.humas_rs['nama'])
        except: self.reg_humas = None 

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'D':
                action_form: str
                image = None
                id_ = None
                self.get_reg_humas(request)
                if self.reg_humas: self.get_reg_rs(self.reg_humas.register_rumahsakit.id)
                
                if self.reg_rs:
                    id_ = self.reg_rs.id
                    action_form = 'rs_activated'
                    form = CreateRumahSakitForm(initial={
                        'nama' : self.reg_rs.nama,
                        'alamat' : self.reg_rs.alamat,
                        'no_telp' : self.reg_rs.no_telp,
                    })
                else:
                    rs = RumahSakit.objects.all().filter(id=self.humas_rs['rumahsakit'])[0]
                    image = rs.image
                    id_ = rs.id
                    action_form = 'rs_change'
                    poliklinik = RumahSakit.objects.values('poliklinik').filter(id=self.humas_rs['rumahsakit'])
                    fasilitas = RumahSakit.objects.values('fasilitas').filter(id=self.humas_rs['rumahsakit'])
                    form = CreateRumahSakitForm(initial={
                        'nama' : rs.nama,
                        'alamat' : rs.alamat,
                        'no_telp' : rs.no_telp,
                        'deskripsi' : rs.deskripsi,
                        'poliklinik' : [poliklinik_['poliklinik'] for poliklinik_ in poliklinik],
                        'fasilitas' : [fasilitas_['fasilitas'] for fasilitas_ in fasilitas],
                        'daerah' : rs.daerah
                    })

                context = {
                    'id' : id_,
                    'action_form' : action_form,
                    'form' : form,
                    'image' : image,
                }
            return redirect('register_rs_list') if request.user.role == 'A' else render(request, 'rumahsakit/index_humas.html', context)
        return render(request, 'index.html') 

class About(View):
    def get(self, request):
        maker = [
             {
                'nama': 'Ganiya Mustafa',
                'image': 'img/about1.jpg',
                'pendidikan': 'SMKN 1 CIMAHI',
                'deskripsi': 'Nama Saya Ganiya Mustafa, disini saya bekerja sebagai Fullstack Developer. Pengalaman saya dalam membuat website ini cukup menyenangkan walaupun memiliki banyak kendala',
                'social': [
                    ['fa-github', 'https://github.com/GaniyaMustafa'],
                    ['fa-linkedin', 'https://www.linkedin.com/in/ganiya-mustafa-83a0b51a0'],
                    ['fa-envelope', 'mailto:ganiyamustaga32@gmail.com']
                ],
             }
            ]

        context = {'abouts': maker}

        return render(request, 'about.html', context)

