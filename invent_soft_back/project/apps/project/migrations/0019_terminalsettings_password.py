# Generated by Django 3.0.2 on 2024-01-18 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_auto_20231114_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminalsettings',
            name='password',
            field=models.CharField(default='444', max_length=10, verbose_name='Пароль редактирования'),
        ),
    ]
