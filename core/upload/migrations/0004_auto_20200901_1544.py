# Generated by Django 2.2.3 on 2020-09-01 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_auto_20200901_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, upload_to='books/covers/'),
        ),
    ]