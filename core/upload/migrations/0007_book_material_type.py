# Generated by Django 3.1 on 2020-09-02 18:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('upload', '0006_remove_book_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='material_type',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
