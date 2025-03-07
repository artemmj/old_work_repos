# Generated by Django 3.2 on 2024-10-14 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0052_alter_templateexport_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateexport',
            name='zone_number_end',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер зоны, до'),
        ),
        migrations.AlterField(
            model_name='templateexport',
            name='zone_number_start',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер зоны, от'),
        ),
    ]
