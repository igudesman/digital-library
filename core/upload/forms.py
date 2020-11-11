from django import forms

from search.models import Tag, Material


class UploadedFileForm(forms.ModelForm):
    """
    Actual form for downloading material
    TODO(add checks like can not download file with the same name)
    """
    class Meta:
        model = Material
        fields = ('title', 'author', 'tags', 'file', )
