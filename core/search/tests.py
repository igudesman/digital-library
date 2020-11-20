# Create your tests here.

import os

from django.core.files import File
from django.test import TestCase
from django.utils import timezone

from .models import Material, Tag


class MyTestCase(TestCase):
    """
    Unit testing of code
    """

    def setUp(self):
        with open('abc.txt', "wb+") as file1, open('qwerty.txt', 'wb+') as file2:
            file1.write('wfwfwe'.encode())
            file2.write('fwrfwe'.encode())

        tag1 = Tag.objects.create(tag="DE")
        tag2 = Tag.objects.create(tag="PS")

        material1 = Material.objects.create(
            who_added_username='admin',
            date_publication=timezone.now(),
            time_publication=timezone.now(),
            title='DE conspects',
            author='Shilov',
            file_name='abc.txt',
            file=File(open('abc.txt', 'rb')),
            visibility='0',
        )

        material2 = Material.objects.create(
            who_added_username='generator',
            date_publication=timezone.now(),
            time_publication=timezone.now(),
            title='PS lecture notes',
            author='Gorod',
            file_name='qwerty.txt',
            file=File(open('qwerty.txt', 'rb')),
            visibility='1',
        )

        material1.tags.set([tag1])
        material1.save()

        material2.tags.set([tag1, tag2])
        material2.save()

        os.remove('abc.txt')
        os.remove('qwerty.txt')

    def test_material_was_created(self):
        material1 = Material.objects.get(title='DE conspects')
        material2 = Material.objects.get(author='Gorod')

        material1.delete()
        material2.delete()

        os.remove('media/abc.txt')
        os.remove('media/qwerty.txt')

        self.assertEqual(material1.author, "Shilov")
        self.assertEqual(material2.title, "PS lecture notes")
