from django.shortcuts import render, redirect
from django.views.generic import View
from dokter.models import Doctor, Spesialis
from rumahsakit.models import RumahSakit, Daerah
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

def paginate_Dokter(data, request):
    page = request.GET.get('page', 1)

    paginator = Paginator(data, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return users

def filter_dokter(request):
    search_text = request.GET.get('dokter')
    spesialis_filter = request.GET.get('spesialis')
    if search_text:
        if spesialis_filter:
            dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(Nama__contains=search_text, spesialis=spesialis_filter).order_by('Nama')[::1]
        else:
            dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(Nama__contains=search_text).order_by('Nama')[::1]
    else:
        if spesialis_filter:
            dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(spesialis=spesialis_filter).order_by('Nama')[::1]
        else:
            dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').order_by('Nama')[::1]
    
    return dokter

class SearchDokter(View):
    def get(self, request):
        dokter = filter_dokter(request)
        spesialis_dokter = Doctor.objects.values('id', 'spesialis').order_by('spesialis')[::1]
        spesialis = Spesialis.objects.all().order_by('spesialis')[::1]

        context = {
            'dokter': paginate_Dokter(dokter, request),
            'spesialis': spesialis,
            'spesialis_dokter' : spesialis_dokter,
        }

        if request.is_ajax():
            html = render_to_string(
                template_name="dokter/dokter-result-partial.html", 
                context = context
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'dokter/index.html', context)

class selectDokter(View):
    def get(self, request, *, dokter_requested):
        dokter = Doctor.objects.values('id', 'Nama', 'image', 'pendidikan', 'pengalaman', 'slug').filter(slug=dokter_requested)[::1]
        hospital = Doctor.objects.values('id', 'rumahsakit').filter(slug=dokter_requested)[::1]
        spesialis_dokter = Doctor.objects.values('id', 'spesialis').filter(slug=dokter_requested).order_by('spesialis')[::1]

        listRS = []
        list_spesialis = []

        for RSlist in hospital:
            listRS.append(RSlist['rumahsakit'])

        for spesialis_list in spesialis_dokter:
            list_spesialis.append(spesialis_list['spesialis'])

        rumahsakit = RumahSakit.objects.all().filter(id__in=listRS).order_by('nama')[::1]
        spesialis = Spesialis.objects.all().filter(id__in=list_spesialis).order_by('spesialis')[::1]
        daerah = Daerah.objects.all().filter(id__in=listRS).order_by('daerah')[::1]

        context = {
            'dokters' : dokter,
            'rumahsakits' : rumahsakit,
            'spesialiss' : spesialis,
            'daerahs' : daerah,
        }

        return render(request, 'dokter/dokter-detail.html', context)

