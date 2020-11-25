from django.shortcuts import render, redirect
from django.views.generic import View

class Index(View):
    def get(self, request):
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
                    ['github.png', 'https://github.com/GaniyaMustafa'],
                    ['linkedin.png', 'www.linkedin.com/in/ganiya-mustafa-83a0b51a0'],
                    ['gmail.png', 'mailto:ganiyamustaga32@gmail.com']
                ],
             }
            ]

        context = {'abouts': maker}

        return render(request, 'about.html', context)

