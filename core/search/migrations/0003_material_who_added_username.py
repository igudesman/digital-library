# Generated by Django 3.1.2 on 2020-10-18 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_material_time_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='who_added_username',
            field=models.CharField(default='admin', max_length=50),
        ),
    ]
