# Generated by Django 3.1.2 on 2020-10-18 06:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='time_publication',
            field=models.TimeField(default=django.utils.timezone.now, help_text='Time of publication'),
            preserve_default=False,
        ),
    ]
