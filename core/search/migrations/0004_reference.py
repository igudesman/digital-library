# Generated by Django 3.1.2 on 2020-10-22 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_material_who_added_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='search.material')),
            ],
        ),
    ]