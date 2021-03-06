from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from search.models import Material, Reference
from .forms import UploadedFileForm


@login_required(redirect_field_name='login')
def upload(request):
    """
    This method generates webpage-form to upload material
    """
    alerts = []
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)

        if form.is_valid():

            material = Material.objects.create(
                who_added_username=request.user.email,
                date_publication=timezone.now(),
                time_publication=timezone.now(),
                title=form.cleaned_data.get('title'),
                author=form.cleaned_data.get('author'),
                file=form.cleaned_data.get('file'),
                file_name=request.FILES['file'],
                visibility='0'
            )

            material.tags.set(form.cleaned_data.get('tags'))
            form = UploadedFileForm()

            material.save()

            reference = Reference.objects.create(reference=material)
            reference.save()
            alerts.insert(0, 'success')

            print("Material:", request.FILES['file'], "was uploaded!")

            return render(request, 'upload/upload.html', context={'form': form, 'alerts': alerts})
        else:
            alerts.insert(0, form.errors)
            print(form.errors)

    else:
        form = UploadedFileForm()

    return render(request, 'upload/upload.html', context={'form': form, 'alerts': alerts})
