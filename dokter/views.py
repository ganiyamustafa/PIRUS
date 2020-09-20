from django.shortcuts import render, redirect
from django.views.generic import View
from dokter.models import Doctor, Spesialis
from rumahsakit.models import RumahSakit
from django.template.loader import render_to_string
from django.http import JsonResponse

def filter_dokter(request):
    search_text = request.GET.get('dokter')
    spesialis_filter = request.GET.get('spesialis')
    print(spesialis_filter)
    if search_text:
        if spesialis_filter:
            dokter = Doctor.objects.all().filter(Nama__contains=search_text, spesialis=spesialis_filter).order_by('Nama')[::1]
        else:
            dokter = Doctor.objects.all().filter(Nama__contains=search_text).order_by('Nama')[::1]
    else:
        if spesialis_filter:
            dokter = Doctor.objects.all().filter(spesialis=spesialis_filter).order_by('Nama')[::1]
        else:
            dokter = Doctor.objects.all().order_by('Nama')[::1]

class SearchDokter(View):
    def get(self, request):
        dokter = filter_dokter(request)
        spesialis = Spesialis.objects.all().order_by('spesialis')[::1]

        context = {
            'dokter': dokter,
            'spesialis': spesialis,
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
        dokter = Doctor.objects.values('id', 'foto').filter(slug=dokter_requested)
        hospital = Doctor.objects.values('id', 'rumahsakit').filter(slug=dokter_requested)

        listRS = []

        for rumahsakit in rumahsakit:
            listRS.append(rumahsakit.rumahsakit)

        rumahsakit = RumahSakit.objects.all().filter(id__in=rs).order_by('nama')[::1]

        return render(request, 'dokter/dokterSelect.html', context)

