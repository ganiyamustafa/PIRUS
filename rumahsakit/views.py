from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from rumahsakit.models import RumahSakit, Daerah, Poliklinik, Fasilitas
from dokter.models import Spesialis, Doctor
from akun.models import DirekturRS
from akun.views import getUserData
from rumahsakit.forms import CreateRumahSakitForm

# def get_rs_data(daerah):
#     rumahsakit = 

#     for rs in rumahsakit:
#         print(rs['nama'])

#     return rumahsakit
def paginate_RS(data, request):
    page = request.GET.get('page', 1)

    paginator = Paginator(data, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return users

def filter_RS(request):
    search_text = request.GET.get('q')
    daerah_filter = request.GET.get('f')

    if search_text:
        if daerah_filter:
            rumahsakit = RumahSakit.objects.values('id', 'nama', 'slug', 'image', 'alamat', 'no_telp', 'daerah').filter(nama__contains=search_text, daerah=daerah_filter).order_by('nama')[::1]
        else:
            rumahsakit = RumahSakit.objects.values('id', 'nama', 'slug', 'image','alamat', 'no_telp', 'daerah').filter(nama__contains=search_text).order_by('nama')[::1]
    else:
        if daerah_filter:
            rumahsakit = RumahSakit.objects.values('id', 'nama', 'slug', 'image','alamat', 'no_telp', 'daerah').filter(daerah=daerah_filter).order_by('nama')[::1]
        else:
            rumahsakit = RumahSakit.objects.values('id', 'nama', 'slug', 'image','alamat', 'no_telp', 'daerah').order_by('nama')[::1]

    return rumahsakit

class searchRS(View):
    def get(self, request):
        rumahsakit = filter_RS(request)
        daerah = Daerah.objects.all().order_by('daerah')[::1]
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
    def filter_dokter(self, request, rs_requst):
        search_text = request.GET.get('dokter')
        spesialis_filter = request.GET.get('spesialis')
        if search_text:
            if spesialis_filter:
                dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(Nama__contains=search_text, spesialis=spesialis_filter, rumahsakit=rs_requst).order_by('Nama')[::1]
            else:
                dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(Nama__contains=search_text, rumahsakit=rs_requst).order_by('Nama')[::1]
        else:
            if spesialis_filter:
                dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(spesialis=spesialis_filter, rumahsakit=rs_requst).order_by('Nama')[::1]
            else:
                dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(rumahsakit=rs_requst).order_by('Nama')[::1]
        
        return dokter

    def get(self, request, *, rs_requested):
        url_request = str(rs_requested).split('/')
        if url_request[0] != 'dokter':
            rumahsakit = RumahSakit.objects.values('id', 'image', 'nama', 'alamat', 'no_telp', 'deskripsi').filter(slug=rs_requested)[::1]
            poliklinikRS = RumahSakit.objects.values('id', 'poliklinik').filter(slug=rs_requested)[::1]
            fasilitasRS = RumahSakit.objects.values('id', 'fasilitas').filter(slug=rs_requested)[::1]
            listpoliklinik = []
            listfasilitas = []
            url = request.path.split('/')[1]
            rs_request = url_request[0]

            for poli in poliklinikRS:
                listpoliklinik.append(poli['poliklinik'])

            for fasil in fasilitasRS:
                listfasilitas.append(fasil['fasilitas'])

            poliklinik = Poliklinik.objects.all().filter(id__in=listpoliklinik)[::1]
            fasilitas = Fasilitas.objects.all().filter(id__in=listfasilitas)[::1]
            context = {
                'rumahsakit': rumahsakit,
                'poliklinik': poliklinik,
                'fasilitas' : fasilitas,
                'url' : url,
                'rs_requested' : rs_request,
                'userdata' : getUserData(request),
            }

            return render(request, 'rumahsakit/rsSelect.html', context)
        elif url_request[0] == 'dokter':
            rs_request = url_request[1]
            rumahsakit = RumahSakit.objects.values('id').filter(slug=rs_request)[::1]
            spesialis_dokters = Doctor.objects.values('id', 'spesialis').filter(rumahsakit=rumahsakit[0]['id'])[::1]
            dokter = self.filter_dokter(request, rumahsakit[0]['id'])
            spesialis_list = []
            
            for spesialis_dokter in spesialis_dokters:
                spesialis_list.append(spesialis_dokter['spesialis'])

            dokter = self.filter_dokter(request, rumahsakit[0]['id'])

            spesialis = Spesialis.objects.all().filter(id__in=spesialis_list).order_by('spesialis')[::1]

            context = {
                'dokter': paginate_RS(dokter, request),
                'spesialis': spesialis,
                'rs_requested' : rs_request,
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
        return super().get(*args, **kwargs) if self.request.user.role == 'A' else redirect('/RumahSakit/')
        

    def get_success_url(self):
        return '/RumahSakit/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class rumahsakitUpdate(UpdateView):
    model = RumahSakit
    form_class = CreateRumahSakitForm

    def get(self, *args, **kwargs):
        authenticated = False
        if self.request.user.role == 'A':
            return super().get(*args, **kwargs)
        elif self.request.user.role == 'D':
            rsuser = DirekturRS.objects.values('id', 'rumahsakit').filter(user=self.request.user.id)
            for direktur in rsuser:
                if direktur['rumahsakit'] == int(self.request.get_full_path().split('/')[1]):
                    authenticated = True
                    break
                else: authenticated = False
            return super().get(*args, **kwargs) if authenticated else redirect('/RumahSakit/')

    def get_success_url(self):
        return '/RumahSakit/'

class rumahsakitDelete(DeleteView):
    model = RumahSakit

    def get(self, *args, **kwargs):
        authenticated = False
        if self.request.user.role == 'A':
            return super().get(*args, **kwargs)
        elif self.request.user.role == 'D':
            rsuser = DirekturRS.objects.values('id', 'rumahsakit').filter(user=self.request.user.id)
            for direktur in rsuser:
                if direktur['rumahsakit'] == int(self.request.get_full_path().split('/')[1]):
                    authenticated = True
                    break
                else: authenticated = False
            return super().get(*args, **kwargs) if authenticated else redirect('/RumahSakit/')

    def get_success_url(self):
        return '/RumahSakit/'