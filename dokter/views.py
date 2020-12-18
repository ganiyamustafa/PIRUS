from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from akun.views import getUserData
from akun.models import DirekturRS
from dokter.models import Doctor, Spesialis
from dokter.forms import CreateDokterForm
from rumahsakit.models import RumahSakit, Daerah

def paginate_Dokter(data, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 6)

    try: users = paginator.page(page)
    except PageNotAnInteger: users = paginator.page(1)
    except EmptyPage: users = paginator.page(paginator.num_pages)

    return users

def filter_dokter(request):
    search_text = request.GET.get('dokter')
    spesialis_filter = request.GET.get('spesialis')
    if search_text:
        if spesialis_filter: dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(Nama__contains=search_text, spesialis=spesialis_filter).order_by('Nama')
        else: dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(Nama__contains=search_text).order_by('Nama')
    else:
        if spesialis_filter: dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(spesialis=spesialis_filter).order_by('Nama')
        else: dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').order_by('Nama')
    
    return dokter

class SearchDokter(View):
    def get(self, request):
        dokter = filter_dokter(request)
        spesialis_dokter = Doctor.objects.values('id', 'spesialis').order_by('spesialis')
        spesialis = Spesialis.objects.all().order_by('spesialis')
        context = {
            'dokter': paginate_Dokter(dokter, request),
            'spesialis': spesialis,
            'spesialis_dokter' : spesialis_dokter,
            'userdata' : getUserData(request),
        }

        if request.is_ajax():
            html = render_to_string(
                template_name="dokter/dokter-result-partial.html", 
                context = context
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'dokter/index.html', context)
    def post(self, request): 
        return redirect('dokter')

class selectDokter(View):
    def get(self, request, *, dokter_requested):
        dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(slug=dokter_requested)
        hospital = Doctor.objects.values('id', 'rumahsakit').filter(slug=dokter_requested)
        spesialis_dokter = Doctor.objects.values('id', 'spesialis').filter(slug=dokter_requested).order_by('spesialis')
        listRS, list_spesialis = [], []

        for RSlist in hospital: listRS.append(RSlist['rumahsakit'])
        for spesialis_list in spesialis_dokter: list_spesialis.append(spesialis_list['spesialis'])

        rumahsakit = RumahSakit.objects.all().filter(id__in=listRS).order_by('nama')
        spesialis = Spesialis.objects.all().filter(id__in=list_spesialis).order_by('spesialis')
        daerah = Daerah.objects.all().filter(id__in=listRS).order_by('daerah')

        context = {
            'dokters' : dokter,
            'rumahsakits' : rumahsakit,
            'spesialiss' : spesialis,
            'daerahs' : daerah,
            'userdata' : getUserData(request),
        }

        return render(request, 'dokter/dokter-detail.html', context)
    def post(self, request, *, dokter_requested): 
        return redirect('dokter-selected', dokter_requested=dokter_requested)

class dokterCreate(CreateView): 
    model = Doctor
    form_class = CreateDokterForm

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs) if self.request.user.role == 'A' else redirect('dokter')
        
    def get_success_url(self):
        return '/dokter/'

class dokterUpdate(UpdateView):
    model = Doctor
    form_class = CreateDokterForm

    def get(self, *args, **kwargs):
        authenticated = False
        if self.request.user.role == 'A': return super().get(*args, **kwargs)
        elif self.request.user.role == 'D':
            rumahsakits = Doctor.objects.values('id', 'rumahsakit').filter(id=int(self.request.get_full_path().split('/')[2]))
            rsuser = DirekturRS.objects.values('id', 'rumahsakit').filter(user=self.request.user.id)

            if rumahsakits:
                for direktur in rsuser:
                    for rumahsakit in rumahsakits:
                        if direktur['rumahsakit'] == rumahsakit['rumahsakit']:
                            authenticated = True
                            break
                        else: authenticated = False
                    if authenticated: break
            else: authenticated = False
            return super().get(*args, **kwargs) if authenticated else redirect('dokter')

    def get_context_data(self, **kwargs):
        context = super(dokterUpdate, self).get_context_data(**kwargs)
        img_dokter = Doctor.objects.values('image').filter(Nama=context['object'])[0]
        context['image'] = img_dokter['image']
        return context

    def get_success_url(self):
        return '/dokter/'

class dokterDelete(DeleteView):
    model = Doctor

    def get(self, *args, **kwargs):
        authenticated = False
        if self.request.user.role == 'A': return super().get(*args, **kwargs)
        elif self.request.user.role == 'D':
            rumahsakit = Doctor.objects.values('id', 'rumahsakit').filter(id=int(self.request.get_full_path().split('/')[2]))
            rsuser = DirekturRS.objects.values('id', 'rumahsakit').filter(user=self.request.user.id)

            if rumahsakits:
                for direktur in rsuser:
                    for rumahsakit in rumahsakits:
                        if direktur['rumahsakit'] == rumahsakit['rumahsakit']:
                            authenticated = True
                            break
                        else: authenticated = False
                    if authenticated: break
            else: authenticated = False
            return super().get(*args, **kwargs) if authenticated else redirect('dokter')

    def get_success_url(self):
        return '/dokter/'

