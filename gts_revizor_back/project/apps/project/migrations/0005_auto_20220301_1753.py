# Generated by Django 3.0.2 on 2022-03-01 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0004_project_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='employees',
        ),
        migrations.AlterField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='manager_projects', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер'),
        ),
    ]
