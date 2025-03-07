# Generated by Django 5.0.4 on 2024-10-23 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_alter_city_options_city_region'),
        ('regions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='regions.region', verbose_name='Регион'),
        ),
    ]
