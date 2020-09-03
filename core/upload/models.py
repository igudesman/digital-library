from django.db import models


class UploadedFile(models.Model):

    STATE_UPLOADED = 0;
    STATE_PROCESSED = 1;
    STATES = [
        (STATE_UPLOADED, 'Uploaded'),
        (STATE_PROCESSED, 'Processed')
    ]

    TYPE_BOOK = 'Book'
    TYPE_LECTURE = 'Lecture'
    TYPE_ASSIGNMENT = 'Assignment'
    TYPES = [
        (TYPE_BOOK, 'Book'),
        (TYPE_LECTURE, 'Lecture'),
        (TYPE_ASSIGNMENT, 'Assignment')
    ]

    status = models.CharField(max_length=20, choices=STATES, default=STATE_UPLOADED)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    material_type = models.CharField(max_length=20, choices=TYPES, default='None')
    file = models.FileField()


    def __str__(self):
        return self.title