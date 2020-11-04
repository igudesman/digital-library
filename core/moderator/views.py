from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
import django_tables2 as tables
from search.models import Material
from django_tables2 import RequestConfig


class MaterialTable(tables.Table):
    T = """<form method="POST" action= {% url 'home'  %}> {% csrf_token %} <input type="submit" class="btn" 
    value="View book"></form> """

    view = tables.TemplateColumn(T)

    class Meta:
        model = Material
        fields = ('title', 'author', 'file_name', "date_publication", "visibility", "who_added_username",)
        template_name = 'django_tables2/bootstrap4.html'


@login_required()
def moder_view(request):
    if not request.user.groups.filter(name='admin').exists():
        return render(request, "not_a_moder.html")
    else:
        table = MaterialTable(Material.objects.all())
        RequestConfig(request).configure(table)
        return render(request, 'moder_material_page.html', {'table': table})
