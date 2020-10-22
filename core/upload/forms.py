from django import forms
from .models import UploadedFile
from search.models import Material, Tag

class UploadedFileForm(forms.Form):
    title = forms.CharField(max_length=50, help_text="title")
    author = forms.CharField(max_length=50, help_text="Author")

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all()
    )

    file = forms.FileField(help_text="Upload material")

    # class Meta:
    #     model = Material
    #     fields = ['title', 'author', 'tags', 'file',]

