# Generated by Django 3.0.2 on 2024-02-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0007_auto_20240206_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='device_model',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Модель терминала'),
        ),
    ]
