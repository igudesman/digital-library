from django.db import models
from django.urls import reverse

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.tag


class Material(models.Model):
    who_added_username = models.CharField(max_length=50, default='admin', null=False)
    date_publication = models.DateField(null=False, help_text="Date of publication")
    time_publication = models.TimeField(null=False, help_text="Time of publication")
    title = models.CharField(max_length=50,null=False, help_text="Title of book")
    author = models.CharField(max_length=50,null=False, help_text="Author")

    tags = models.ManyToManyField(Tag, help_text="Tags of book")

    file = models.FileField(null=False, help_text="File with material")

    file_name = models.CharField(max_length=50,null=False,  help_text="Name of file")

    STATES = [
        ('0', 'Uploaded'),
        ('1', 'Processed')
    ]

    visibility = models.CharField(max_length=1, choices=STATES, default='0', null=False, help_text="state of book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('material-detail', args=[str(self.id)])