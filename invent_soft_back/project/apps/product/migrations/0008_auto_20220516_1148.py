# Generated by Django 3.0.2 on 2022-05-16 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20220511_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='am',
            field=models.CharField(blank=True, max_length=127, null=True, verbose_name='Акцизная марка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='dm',
            field=models.CharField(blank=True, max_length=127, null=True, verbose_name='Датаматрикс'),
        ),
    ]
