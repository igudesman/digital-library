
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, Http404
from django.views import generic
from search.models import Material
from search.views import get_material_queryset
from operator import attrgetter

def home_view(request):
    """
    Generates home view. If search request is empty, shows all material that in the site (visibility='1')
    """
    context = {}

    query = ""
    if request.POST:
        print(request.POST)
        query = request.POST.get('search_field', "")
        context['query'] = str(query)

    if query == "":
        print("Empty request")
        material_list = sorted(Material.objects.filter(visibility__icontains='1').all(), key=attrgetter('date_publication'), reverse=True)
    else:
        material_list = sorted(get_material_queryset(query), key=attrgetter('date_publication'), reverse=True)
    context['material_list'] = material_list
    return render(request, 'home/home.html', context)


class MaterialDetailView(generic.DetailView):
    model = Material