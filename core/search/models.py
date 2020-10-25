from django.db import models
from django.urls import reverse

# Create your models here.
# Our main tables, databases
class Tag(models.Model):
    """
    Table for storing tags (with courses labels or simple genres). One material - many or none tags
    """
    tag = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.tag


class Material(models.Model):
    """
    Table for storing materials.
    TODO(we dont need time_publication - django timezone already stores time and date)
    """
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

    # For showing url of book, idk how it works
    def get_absolute_url(self):
        return reverse('material-detail', args=[str(self.id)])


class Reference(models.Model):
    """
    With creation of material we create request to the material
    """
    reference = models.OneToOneField(Material, on_delete=models.CASCADE)