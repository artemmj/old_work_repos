# Generated by Django 3.0.2 on 2023-11-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_terminalsettings_manual_input_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rmmsettings',
            name='password',
            field=models.CharField(blank=True, default='555', max_length=10, null=True, verbose_name='Пароль для редактирования настроек'),
        ),
    ]
