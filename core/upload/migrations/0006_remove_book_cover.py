# Generated by Django 3.1 on 2020-09-02 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_auto_20200902_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='cover',
        ),
    ]