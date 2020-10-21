from django import forms
from .models import UploadedFile
from search.models import Material

class UploadedFileForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = ('title', 'author', 'tags', 'file',)
