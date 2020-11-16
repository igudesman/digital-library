import django_tables2 as tables
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_tables2 import RequestConfig

from search.models import Material


# Create your views here.


class MaterialTable(tables.Table):
    T1 = '<a href="/material/{{record.id}}">View book</a>'
    T2 = '<a href="/material/change_visibility/{{record.id}}">Change visibility</a>'
    T3 = '<a href="/material/delete/{{record.id}}">Delete book</a>'

    c1 = tables.TemplateColumn(T1)
    c2 = tables.TemplateColumn(T2)
    c3 = tables.TemplateColumn(T3)

    class Meta:
        model = Material
        fields = ('title', 'author', 'file_name', "date_publication", "visibility", "who_added_username",)
        template_name = 'django_tables2/bootstrap4.html'


@login_required(redirect_field_name='login')
def moder_view(request):
    if not request.user.groups.filter(name='admin').exists():
        return render(request, "not_a_moder.html")
    else:
        table = MaterialTable(Material.objects.all().order_by('visibility'))
        RequestConfig(request).configure(table)
        return render(request, 'moder_material_page.html', {'table': table})
