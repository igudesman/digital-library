from django.http import StreamingHttpResponse, Http404, HttpResponse, FileResponse
from django.shortcuts import render
from .models import Material
from django.db.models import Q
import os


# Create your views here.


# Word by word finding matches
def get_material_queryset(query=None):
    queryset = []

    queries = query.split(" ")  # Split query into words

    for q in queries:
        materials = Material.objects.filter(
            (Q(title__icontains=q) |
             Q(author__icontains=q) |
             Q(file_name__icontains=q) |
             Q(author__icontains=q) |
             Q(tags__tag=q)) &
            Q(visibility__icontains='1')
        ).distinct()

        for material in materials:
            queryset.append(material)

    return list(set(queryset))


def file_download(request, file_path):
    print(file_path)
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404

def material_page(request, material_id):
    context = {}
    material = Material.objects.filter(pk=material_id)
    context['material'] = material[0]
    return render(request, 'search/material_detail.html', context)
