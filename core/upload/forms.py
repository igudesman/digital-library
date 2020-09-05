from django import forms
from .models import UploadedFile


class UploadedFileForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ('title', 'author', 'material_type', 'file')

    def validate_file_type(self, extension, file_type):

        BOOK_TYPES = ['pdf', 'txt', 'epub']
        LECTURE_TYPES = ['pdf']
        ASSIGNMENT_TYPES = ['pdf']

        if (file_type == 'Book') and (extension in BOOK_TYPES):
            return True
        elif (file_type == 'Lecture') and (extension in LECTURE_TYPES):
            return True
        elif (file_type == 'Assignment') and (extension in ASSIGNMENT_TYPES):
            return True
        return False