import os
from operator import attrgetter

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import Http404, FileResponse
from django.shortcuts import render

from .models import Material


# Create your views here.

def is_moder(user):
    return user.groups.filter(name='admin').exists()


# Word by word finding matches
from moderator.views import moder_view


def get_material_queryset(query, category):
    """
    Retrieve all materials by the query in search bar
    """

    # Self checking
    assert category == 'Title' or category == 'All categories' or category == 'Tags' or category=='Author'
    queryset = []

    queries = query.split(" ")  # Split query into words

    for q in queries:
        materials = None
        print("category", category)

        if category == 'All categories':
            materials = Material.objects.filter(visibility='1').filter(
                Q(title__icontains=q) |
                Q(author__icontains=q) |
                Q(tags__tag=q)
            )

        elif category == 'Title':
            materials = Material.objects.filter(visibility='1').filter(
                Q(title__icontains=q)
            )

        elif category == 'Tags':
            materials = Material.objects.filter(visibility='1').filter(
                Q(tags__tag=q)
            )
        else:
            materials = Material.objects.filter(visibility='1').filter(
                Q(author__icontains=q)
            )


        for material in materials:
            queryset.append(material)

    queryset = sorted(list(set(queryset)), key=attrgetter('time_publication'), reverse=True)

    return queryset


@login_required(redirect_field_name='login')
def file_download(request, file_path):
    file_path = file_path[1:]
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404


@login_required(redirect_field_name='login')
def material_page(request, material_id):
    context = {}
    material = Material.objects.get(pk=material_id)
    return render(request, 'search/material_detail.html', {'material': material})


@login_required(redirect_field_name='login')
@user_passes_test(is_moder)
def change_view(request, material_id):
    if not request.user.groups.filter(name='admin').exists():
        return render(request, "not_a_moder.html")

    material = Material.objects.get(pk=material_id)
    material.visibility = "0" if material.visibility == "1" else "1"
    material.save()
    return moder_view(request)


@login_required(redirect_field_name='login')
@user_passes_test(is_moder)
def delete_view(request, material_id):
    if not request.user.groups.filter(name='admin').exists():
        return render(request, "not_a_moder.html")

    material = Material.objects.get(pk=material_id)
    material.delete()
    return moder_view(request)


def is_moder(user):
    return user.groups.filter(name='admin').exists()
