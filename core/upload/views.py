from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import UploadedFileForm
from .models import UploadedFile

def upload(request):
    context = {}
    if request.method == 'POST':
        file_name = request.FILES['file']
        file_type = request.POST['material_type']
        file_extension = ''

        form = UploadedFileForm(request.POST, request.FILES)
        try:
            file_extension = (str(file_name)).split('.')[-1]
            print(type(file_name))
            if not form.validate_file_type(file_extension, file_type):
                print('SHIT1!') # TODO
        except ValueError:
        	print('SHIT2!') # TODO
        if form.is_valid():
            form.save()

    else:
        form = UploadedFileForm()
    return render(request, 'upload/upload.html', context)