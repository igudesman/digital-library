from django.shortcuts import render
from .models import Material
from django.db.models import Q
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
            Q(author__icontains=q)) &
            Q(visibility__icontains='1')
        ).distinct()

        for material in materials:
            queryset.append(material)

    return list(set(queryset))

