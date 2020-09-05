from django.shortcuts import render
from django.http import HttpResponse
from upload.models import UploadedFile

def home(request):
    context = parse_data()
    return render(request, 'home/home.html', context)


def parse_data():
    context = {'Book': [],
               'Lecture': [],
               'Assignment': []}
    content = UploadedFile.objects.all()
    for material in content:
        context[str(material.material_type)].append(material)
    return context

