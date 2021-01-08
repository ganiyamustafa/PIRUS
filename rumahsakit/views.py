from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from rumahsakit.models import RumahSakit, Daerah, Poliklinik, Fasilitas
from rumahsakit.forms import CreateRumahSakitForm
from dokter.models import Spesialis, Doctor
from akun.models import DirekturRS
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