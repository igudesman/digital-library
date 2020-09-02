from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import BookForm
from .models import Book

def upload(request):
    context = {}
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
        	form.save()
    else:
    	form = BookForm()
    return render(request, 'upload/upload.html', context)