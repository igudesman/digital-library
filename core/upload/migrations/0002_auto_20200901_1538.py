# Generated by Django 2.2.3 on 2020-09-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(upload_to='books/covers/'),
        ),
    ]
