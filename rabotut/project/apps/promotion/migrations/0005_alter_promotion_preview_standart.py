# Generated by Django 5.0.4 on 2024-09-09 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_image'),
        ('promotion', '0004_remove_promotion_cover_promotion_preview_main_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='preview_standart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preview_standart_promotion', to='file.image', verbose_name='Превью стандарт'),
        ),
    ]
