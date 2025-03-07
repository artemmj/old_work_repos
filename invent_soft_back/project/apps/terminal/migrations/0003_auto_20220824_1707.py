# Generated by Django 3.0.2 on 2022-08-24 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20220816_1615'),
        ('terminal', '0002_terminal_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='employee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='terminal', to='employee.Employee', verbose_name='Сотрудник'),
        ),
    ]
