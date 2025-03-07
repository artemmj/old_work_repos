# Generated by Django 3.0.2 on 2022-04-29 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20220429_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(choices=[('for_the_client', 'Для заказчика'), ('products_catalog_load', 'Загружен справочник/каталог'), ('products_catalog_delete', 'Удален справочник/каталог'), ('zones_delete', 'Удалены зоны'), ('create_new_project', 'Создан новый проект'), ('project_settings_load', 'Загружены настройки проекта'), ('terminal_settings_update', 'Обновлены настройки терминала')], default='for_the_client', max_length=24, verbose_name='Название события'),
        ),
    ]
