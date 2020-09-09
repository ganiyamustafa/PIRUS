from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import render_to_string
from django.http import JsonResponse
from rumahsakit.models import RumahSakit, Daerah

# def get_rs_data(daerah):
#     rumahsakit = 

#     for rs in rumahsakit:
#         print(rs['nama'])

#     return rumahsakit

def ListRS(request):        
    context = {
        'RumahSakit': RumahSakit.objects.values('id', 'nama').filter(daerah=1).order_by('nama')[::1]
    }
    return render(request, 'rumahsakit/index.html', context)

def SearchRS(request):
    if request.method == "GET":
        search_text = request.GET.get('q')
        daerah_filter = request.GET.get('f')

        if search_text:
            if daerah_filter:
                rumahsakit = RumahSakit.objects.values('id', 'nama').filter(nama__contains=search_text, daerah=daerah_filter).order_by('nama')[::1]
            else:
                rumahsakit = RumahSakit.objects.values('id', 'nama').filter(nama__contains=search_text).order_by('nama')[::1]
        else:
            if daerah_filter:
                rumahsakit = RumahSakit.objects.values('id', 'nama').filter(daerah=daerah_filter).order_by('nama')[::1]
            else:
                rumahsakit = RumahSakit.objects.values('id', 'nama').order_by('nama')[::1]
        daerah = Daerah.objects.all().order_by('daerah')[::1]

        context = {
            'RumahSakit': rumahsakit,
            'daerah' : daerah,
        }

        if request.is_ajax():
            html = render_to_string(
                template_name="rumahsakit/rumahsakit-result-partial.html", 
                context = context
            )

            print(rumahsakit)

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'rumahsakit/index.html', context)