# Generated by Django 5.0.4 on 2024-10-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0005_alter_storiesmailinguserrole_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='storiesmailingregion',
            name='to_all_regions',
            field=models.BooleanField(blank=True, null=True, verbose_name='Рассылка на все регионы'),
        ),
    ]
