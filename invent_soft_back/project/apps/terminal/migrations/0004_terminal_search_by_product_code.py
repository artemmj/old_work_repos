# Generated by Django 3.0.2 on 2022-09-15 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0003_auto_20220824_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='search_by_product_code',
            field=models.BooleanField(default=False, verbose_name='Поиск по коду товара'),
        ),
    ]
