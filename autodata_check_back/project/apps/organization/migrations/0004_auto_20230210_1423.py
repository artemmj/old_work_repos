# Generated by Django 3.0.2 on 2023-02-10 11:23

import apps.helpers.inn_validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20230208_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Вкл/Выкл'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='inn',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True, validators=[apps.helpers.inn_validator.inn_validator], verbose_name='ИНН'),
        ),
    ]
