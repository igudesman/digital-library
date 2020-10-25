from django import forms
from search.models import Material, Tag

class UploadedFileForm(forms.Form):
    """
    Actual form for downmloading material
    TODO(add checks like can not download file with the same name)
    """
    title = forms.CharField(max_length=50, help_text="title")
    author = forms.CharField(max_length=50, help_text="Author")

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all()
    )

    file = forms.FileField(help_text="Upload material")

