# Generated by Django 3.0.2 on 2024-03-14 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_product_store_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='store_number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер магазина (для РеТрейдинг)'),
        ),
    ]
