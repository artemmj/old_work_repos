# Generated by Django 3.0.2 on 2023-12-13 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_scannedproduct_is_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='remainder',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=11, verbose_name='Остаток'),
        ),
    ]
