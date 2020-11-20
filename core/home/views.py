from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from search.models import Material
from search.views import get_material_queryset


@login_required(redirect_field_name='login')
def my_logout(request):
    logout(request)
    return render(request, "info_message.html", {'message': "You have been successfully logout!"})


def home_view(request):
    """
    Generates home view. If search request is empty, shows all material that in the site (visibility='1')
    """
    context = {}

    query, category = "", "All categories"
    if request.POST:
        query = request.POST.get('search_field', "")
        category = request.POST.get('choices-single-defaul', 'All categories')

    context['material_list'] = get_material_queryset(query, category)

    return render(request, 'new_home.html', context)


class MaterialDetailView(generic.DetailView):
    model = Material
