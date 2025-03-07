# Generated by Django 3.0.2 on 2023-08-17 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('template', '0013_auto_20230816_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templateinvitation',
            name='owner',
        ),
        migrations.AlterField(
            model_name='templateinvitation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='template_invitations', to=settings.AUTH_USER_MODEL, verbose_name='приглашаемый пользователь'),
        ),
    ]
