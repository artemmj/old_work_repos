# Generated by Django 3.0.2 on 2024-01-23 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_terminalsettings_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='auto_assign_enbale',
        ),
    ]
