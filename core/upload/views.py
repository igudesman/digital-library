from django.shortcuts import render
from .forms import UploadedFileForm
from search.models import Material, Reference
import datetime

from home.views import home_view

from django.contrib.auth.decorators import login_required


@login_required
def upload(request):
    """
    This method generates webpage-form to upload material
    """
    if request.method == 'POST':
        print("POST")
        form = UploadedFileForm(request.POST, request.FILES)

        print("Errors: ", form.errors)

        if form.is_valid():
            material = Material.objects.create(
                who_added_username='Will add later',
                date_publication=datetime.datetime.now(),
                time_publication=datetime.datetime.now(),
                title=form.cleaned_data.get('title'),
                author=form.cleaned_data.get('author'),
                file=form.cleaned_data.get('file'),
                file_name=request.FILES['file'],
                visibility='0'
            )

            material.tags.set(form.cleaned_data.get('tags'))

            material.save()

            reference = Reference.objects.create(reference=material)
            reference.save()

            print("Material:", request.FILES['file'], "was uploaded!")

            return home_view(request)

    else:
        form = UploadedFileForm()

    return render(request, 'upload/upload.html', context={'form': form})
