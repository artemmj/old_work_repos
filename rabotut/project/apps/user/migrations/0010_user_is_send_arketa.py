# Generated by Django 5.0.4 on 2024-12-05 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_user_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_send_arketa',
            field=models.BooleanField(default=False, verbose_name='Создание в аркете'),
        ),
    ]
