# Generated by Django 3.0.2 on 2022-11-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0011_auto_20221108_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='tsd_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='№ ТСД'),
        ),
    ]
