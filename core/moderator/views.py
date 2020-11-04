from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from search.models import Material

@login_required()
def moder_view(request):
    materials = Material.objects.filter(visibility__icontains='0').distinct()
    return render(request, 'moder_material_page.html', {'materials': materials})
