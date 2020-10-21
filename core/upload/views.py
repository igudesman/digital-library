from django.shortcuts import render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .forms import UploadedFileForm
from .models import UploadedFile
from search.models import Material
import datetime

from home.views import home_view


# def upload(request):
#     status = True
#     context = {'title': '',
#                'author': '',
#                'material_type': ''}
#
#     if request.method == 'POST':
#         file_name = request.FILES['file']
#         file_extension = ''
#
#         form = UploadedFileForm(request.POST, request.FILES)
#         try:
#             file_extension = (str(file_name)).split('.')[-1]
#             print(type(file_name))
#             if not form.validate_file_type(file_extension, file_type):
#                 messages.error(request, '{0} file extension is not supported for {1} material! Please, try again'.format(file_extension, file_type))
#                 context['title'] = request.POST['title']
#                 context['author'] = request.POST['author']
#                 context['material_type'] = request.POST['material_type']
#                 status = False
#         except ValueError:
#             messages.error(request, 'Something went wrong!')
#             status = False
#         if form.is_valid() and status:
#             form.save()
#
#             assert request.user.is_authentificated()
#             model = Material(
#                 who_added_username=request.user,
#                 date_publication=datetime.now(),
#                 time_publication=datetime.now(),
#                 title=context['title'],
#                 author=context['author'],
#
#             )
#             messages.success(request, '{0} {1} has been successefully added!'.format(file_type, file_name))
#     else:
#         form = UploadedFileForm()
#
#
#     return render(request, 'upload/upload.html', context)


def upload(request):
    form = UploadedFileForm()

    if form.is_valid():
        name = None
        for filename, file in request.FILES.iteritems():
            name = request.FILES[filename].name

        material = Material.objects.create(
            who_added_username='Will add later',
            date_publication=datetime.datetime.now(),
            time_publication=datetime.datetime.now(),
            title=form.cleaned_data.get('title'),
            author=form.cleaned_data.get('author'),
            tags=form.cleaned_data.get('tags'),
            file=form.cleaned_data.get('file'),
            file_name=name,
            visibility='0'
        )

        material.save()

        print("Material:", name, "was uploaded!")

        return home_view(request)

    return render(request, 'upload.html', context={'form': form})