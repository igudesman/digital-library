from django.http import StreamingHttpResponse, Http404, HttpResponse, FileResponse
from django.shortcuts import render
from .models import Material
from django.db.models import Q
import os

# Create your views here.
# TODO( сделать нормальну закрузку материалов, а не то, что у нас)

# Word by word finding matches
from moderator.views import moder_view


def get_material_queryset(query=None):
    """
    Retrieve all materials bu the query in search bar
    """
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
    file_path = file_path[1:]
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


def change_view(request, material_id):
    if not request.user.groups.filter(name='admin').exists():
        return render(request, "not_a_moder.html")

    material = Material.objects.get(pk=material_id)
    material.visibility = "0" if material.visibility == "1" else "1"
    material.save()
    return moder_view(request)


def delete_view(request, material_id):
    if not request.user.groups.filter(name='admin').exists():
        return render(request, "not_a_moder.html")

    material = Material.objects.get(pk=material_id)
    material.delete()
    return moder_view(request)
