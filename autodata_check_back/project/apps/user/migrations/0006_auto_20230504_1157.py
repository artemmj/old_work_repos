# Generated by Django 3.0.2 on 2023-05-04 08:57

import apps.helpers.model_fields
import apps.user.models.user
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20230228_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=apps.helpers.model_fields.ChoiceArrayField(base_field=models.CharField(choices=[('customer', 'Заказчик'), ('inspector', 'Инспектор'), ('dispatcher', 'Диспетчер'), ('administrator', 'Администратор')], default='customer', max_length=13, verbose_name='Роль'), default=apps.user.models.user.get_default_role, size=None, verbose_name='Роли'),
        ),
    ]
