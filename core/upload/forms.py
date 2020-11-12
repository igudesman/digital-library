import os

from django import forms
from django.core.exceptions import ValidationError

from search.models import Material


class UploadedFileForm(forms.ModelForm):
    """
    Actual form for downloading material
    TODO(add checks like can not download file with the same name)
    """

    class Meta:
        model = Material
        fields = ('title', 'author', 'tags', 'file',)

    def clean_file(self):
        super().clean()
        file = self.cleaned_data.get('file')
        filename: str = os.path.basename(file.name)

        # File size < 10 mb
        if file.size > 10 * 1024 * 1024:
            raise ValidationError(f'The size of book" {file.size} exceeds 10 mb!')

        if not filename.endswith('.pdf') and not filename.endswith('.djvu') \
                and not filename.endswith('.doc') and not filename.endswith('.docx'):
            raise ValidationError("format is not supported, please convert it into .pdf or .doc or")

        if Material.objects.filter(file_name=filename).exists():
            raise ValidationError(f'This book is already uploaded to website!')

        return file

    def clean_title(self):
        super().clean()
        title = self.cleaned_data.get('title')
        if Material.objects.filter(title='title').exists():
            raise ValidationError(f"The book with this title: {title} already exists in database!")

        return title
