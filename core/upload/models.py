from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    material_type = models.CharField(max_length=100, default='None')
    file = models.FileField(default=None)


    def __str__(self):
        return self.title