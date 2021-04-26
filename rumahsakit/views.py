import string, random
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from rumahsakit.models import RumahSakit, Daerah, Poliklinik, Fasilitas, RegisterHUMASRS, RegisterRumahSakit
from rumahsakit.forms import CreateRumahSakitForm, RegisterRumahSakitForm, RegisterHUMASRSForm
from dokter.models import Spesialis, Doctor
from akun.models import DirekturRS, CustomUser
from akun.views import getUserData

def check_auth(self):
    rsuser = DirekturRS.objects.values('id', 'rumahsakit').filter(user=self.request.user.id)
    rumahsakit_id = [direktur['rumahsakit'] for direktur in rsuser]
    rumahsakit_id_confirm = [int(self.request.get_full_path().split('/')[2])]
    if any(item in rumahsakit_id_confirm for item in rumahsakit_id): authenticated = True
    else: authenticated = False
    return authenticated

def paginate_RS(data, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 6)
    try: users = paginator.page(page)
    except PageNotAnInteger: users = paginator.page(1)
    except EmptyPage: users = paginator.page(paginator.num_pages)

    return users

def filter_RS(request):
    search_text = request.GET.get('q')
    daerah_filter = request.GET.get('f')
    if search_text:
        if daerah_filter: rumahsakit = RumahSakit.objects.values('id', 'nama', 'slug', 'image', 'alamat', 'no_telp', 'daerah').filter(nama__contains=search_text, daerah=daerah_filter).order_by('nama')[::1]
        else: rumahsakit = RumahSakit.objects.values('id', 'nama', 'slug', 'image','alamat', 'no_telp', 'daerah').filter(nama__contains=search_text).order_by('nama')[::1]
    else:
        if daerah_filter: rumahsakit = RumahSakit.objects.values('id', 'nama', 'slug', 'image','alamat', 'no_telp', 'daerah').filter(daerah=daerah_filter).order_by('nama')[::1]
        else: rumahsakit = RumahSakit.objects.values('id', 'nama', 'slug', 'image','alamat', 'no_telp', 'daerah').order_by('nama')[::1]

    return rumahsakit

class searchRS(View):
    def get(self, request):
        rumahsakit = filter_RS(request)
        daerah = Daerah.objects.all().order_by('daerah')
        context = {
            'daerah' : daerah,
            'RumahSakit' : paginate_RS(rumahsakit, request),
            'userdata' : getUserData(request),
        }
        if request.is_ajax():
            html = render_to_string(
                template_name="rumahsakit/rumahsakit-result-partial.html", 
                context = context
            )
            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'rumahsakit/index.html', context)
    def post(self, request):
        return redirect('RumahSakit')

class selectRS(View):
    def get(self, request, *, rs_requested):
        rumahsakit = RumahSakit.objects.values('id', 'image', 'nama', 'alamat', 'no_telp', 'deskripsi').filter(slug=rs_requested)
        poliklinikRS = RumahSakit.objects.values('id', 'poliklinik').filter(slug=rs_requested)
        fasilitasRS = RumahSakit.objects.values('id', 'fasilitas').filter(slug=rs_requested)
        listpoliklinik, listfasilitas = [], []

        for poli in poliklinikRS: listpoliklinik.append(poli['poliklinik'])
        for fasil in fasilitasRS: listfasilitas.append(fasil['fasilitas'])

        poliklinik = Poliklinik.objects.all().filter(id__in=listpoliklinik)
        fasilitas = Fasilitas.objects.all().filter(id__in=listfasilitas)
        context = {
            'rumahsakit': rumahsakit,
            'poliklinik': poliklinik,
            'fasilitas' : fasilitas,
            'rs_requested': rs_requested,
            'userdata' : getUserData(request),
        }

        return render(request, 'rumahsakit/rsSelect.html', context)

class register_rumahsakit_step1(CreateView):
    global step
    step = 1
    model = RegisterRumahSakit
    form_class = RegisterRumahSakitForm

    def form_valid(self, form):
        global nama_rs 
        nama_rs = form.instance.nama
        return super(register_rumahsakit_step1, self).form_valid(form)

    def get_success_url(self):
        global step
        step = 2
        return '/rumahsakit/register/2/'

class register_rumahsakit_step2(CreateView):
    model = RegisterHUMASRS
    form_class = RegisterHUMASRSForm

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs) if step and step == 2 else redirect('register_rs_1')

    def form_valid(self, form):
        global nama_humas 
        nama_humas = form.instance.nama
        return super(register_rumahsakit_step2, self).form_valid(form)

    def get_success_url(self):
        global step
        step = 3
        return '/rumahsakit/register/3/'

class register_rumahsakit_step3(View):
        
    def get(self, request):
        if step == 3:
            # update reg_rs
            register_rs = RegisterRumahSakit.objects.get(nama=nama_rs)
            register_rs.is_finish_registered = True
            register_rs.save()
            # update reg_humas
            register_humas = RegisterHUMASRS.objects.get(nama=nama_humas)
            register_humas.register_rumahsakit = register_rs
            register_humas.save()

            return render(request, 'rumahsakit/register_rumahsakit/register_rumahsakit_step3.html')
        else: return redirect('register_rs_1')

class register_rumahsakit_lists(View):
    def get(self, request):
        reg_rs = RegisterRumahSakit.objects.all().filter(is_finish_registered=True, is_accepted=False).order_by('nama')
        reg_humas = RegisterHUMASRS.objects.values('id', 'nama', 'email', 'no_telp', 'foto_diri', 'foto_ktp', 'register_rumahsakit').order_by('nama')
        context = {
            'register_rs_lists' : reg_rs,
            'register_humas_lists' : reg_humas,
        }
        return render(request, 'rumahsakit/register_rumahsakit_admin.html', context)

class register_rumahsakit_denied(View):
    def get(self, request, pk):
        reg_rs = RegisterRumahSakit.objects.get(id=pk)
        reg_rs.delete()
        return redirect('register_rs_list')

class register_rumahsakit_accepted(View):
    username_ = password_ = reg_rs = reg_humas = humas_rs = user_ = ''
    def random_username_password(self):
        pass_type = [1,2]
        for a in range(0,8): 
            if random.choice(pass_type) % 2 == 0: self.password_ += str(random.randint(0,9))
            else: self.password_ += random.choice(string.ascii_letters)
        for a in range(0,5): self.username_ += random.choice(string.ascii_letters)

    def register_rumahsakit_updated(self, pk):
        self.reg_rs = RegisterRumahSakit.objects.get(id=pk)
        self.reg_rs.is_accepted = True
        self.reg_rs.save()

    def create_account(self):
        self.user_ = CustomUser(username=self.username_, role='D')
        self.user_.set_password(self.password_)
        self.user_.save()

    def create_humas_data(self, pk):
        self.reg_humas = RegisterHUMASRS.objects.get(register_rumahsakit=self.reg_rs)
        self.humas_rs = DirekturRS.objects.create(
            user = self.user_,
            nama = self.reg_humas.nama,
            no_telp = self.reg_humas.no_telp,
            email = self.reg_humas.email,
        )
        self.humas_rs.rumahsakit.set(RegisterRumahSakit.objects.filter(id__in=pk))
        self.humas_rs.save()

    def send_email(self):
        subject, from_email, to = 'tes', 'pirus.apl@gmail.com', 'ganiyamustaga32@gmail.com'
        text_content = 'tes'
        context = { 
                    'name': self.reg_humas.nama,
                    'rumahsakit': self.reg_rs.nama,
                    'username': self.username_,
                    'password': self.password_,
                  }
        html_content = render_to_string('email_accepted.html', context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    def get(self, request, pk):
        self.random_username_password()
        self.register_rumahsakit_updated(pk)
        self.create_account()
        self.create_humas_data(pk)
        self.send_email()
        return redirect('register_rs_list')

class rumahsakit_activated(View):
    def get(self, request, pk):
        pass

    def post(self, request, pk):
        reg_rs = RegisterRumahSakit.objects.get(id=pk)
        humas_rs = DirekturRS.objects.get(user=request.user.id)
        daerah = Daerah.objects.get(id=request.POST.get('daerah'))
        rumahsakit = RumahSakit.objects.create(
            nama = request.POST.get('nama'),
            alamat = request.POST.get('alamat'),
            no_telp = request.POST.get('no_telp'),
            deskripsi = request.POST.get('deskripsi'),
            daerah = daerah,
            image = request.FILES['image'],
        )
        rumahsakit.poliklinik.set(request.POST.get('poliklinik'))
        rumahsakit.fasilitas.set(request.POST.get('poliklinik'))
        rumahsakit.save()
        humas_rs.rumahsakit.set(RumahSakit.objects.filter(id=rumahsakit.id))
        humas_rs.save()
        reg_rs.delete()
        return redirect('/')



class rumahsakit_changed(View):
    def get(self, request, pk):
        pass

    def post(self, request, pk):
        daerah = Daerah.objects.get(id=request.POST.get('daerah'))
        rumahsakit = RumahSakit.objects.get(id=pk)
        rumahsakit.nama = request.POST.get('nama')
        rumahsakit.alamat = request.POST.get('alamat')
        rumahsakit.no_telp = request.POST.get('no_telp')
        rumahsakit.deskripsi = request.POST.get('deskripsi')
        rumahsakit.daerah = daerah
        if request.FILES: rumahsakit.image = request.FILES['image']
        rumahsakit.poliklinik.set(request.POST.get('poliklinik'))
        rumahsakit.fasilitas.set(request.POST.get('poliklinik'))
        rumahsakit.save()
        return redirect('/')


class rumahsakit_dokter(View):
    def filter_dokter(self, request, rs_requst):
        search_text = request.GET.get('dokter')
        spesialis_filter = request.GET.get('spesialis')
        if search_text:
            if spesialis_filter: dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(Nama__contains=search_text, spesialis=spesialis_filter, rumahsakit=rs_requst).order_by('Nama')
            else: dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(Nama__contains=search_text, rumahsakit=rs_requst).order_by('Nama')
        else:
            if spesialis_filter: dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(spesialis=spesialis_filter, rumahsakit=rs_requst).order_by('Nama')
            else: dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(rumahsakit=rs_requst).order_by('Nama')
        
        return dokter

    def get(self, request, *, rs_requested):
        rumahsakit = RumahSakit.objects.values('id').filter(slug=rs_requested)
        spesialis_dokters = Doctor.objects.values('id', 'spesialis').filter(rumahsakit=rumahsakit[0]['id'])
        dokter = self.filter_dokter(request, rumahsakit[0]['id'])
        spesialis_list = []
        
        for spesialis_dokter in spesialis_dokters: spesialis_list.append(spesialis_dokter['spesialis'])

        dokter = self.filter_dokter(request, rumahsakit[0]['id'])
        spesialis = Spesialis.objects.all().filter(id__in=spesialis_list).order_by('spesialis')
        context = {
            'dokter': paginate_RS(dokter, request),
            'spesialis': spesialis,
            'rs_requested': rs_requested,
            'rumahsakits' : rumahsakit,
            'spesialis_dokter': spesialis_dokters,
            'userdata' : getUserData(request),
        }

        if request.is_ajax():
            html = render_to_string(
                template_name="dokter/dokter-result-partial.html", 
                context = context
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'rumahsakit/dokterRsSelect.html', context)

class rumahsakitCreate(CreateView): 
    model = RumahSakit
    form_class = CreateRumahSakitForm

    def get(self, *args, **kwargs):
        authenticated = False
        return super().get(*args, **kwargs) if self.request.user.role == 'A' else redirect('rumahsakit')

    def get_success_url(self):
        return '/rumahsakit/'

class rumahsakitUpdate(UpdateView):
    model = RumahSakit
    form_class = CreateRumahSakitForm

    def get(self, *args, **kwargs):
        authenticated = False
        if self.request.user.role == 'A': return super().get(*args, **kwargs)
        elif self.request.user.role == 'D': return super().get(*args, **kwargs) if check_auth(self) else redirect('rumahsakit')

    def get_context_data(self, **kwargs):
        context = super(rumahsakitUpdate, self).get_context_data(**kwargs)
        image_rumahsakit = RumahSakit.objects.values('image').filter(nama=context['object'])[0]
        context['image'] = image_rumahsakit['image']
        return context

    def get_success_url(self):
        return '/rumahsakit/'

class rumahsakitDelete(DeleteView):
    model = RumahSakit

    def get(self, *args, **kwargs):
        authenticated = False
        if self.request.user.role == 'A': return super().get(*args, **kwargs)
        elif self.request.user.role == 'D': return super().get(*args, **kwargs) if check_auth(self) else redirect('rumahsakit')

    def get_success_url(self):
        return '/rumahsakit/'