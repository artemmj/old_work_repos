# Generated by Django 3.0.2 on 2023-10-30 09:48

import apps.helpers.model_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0012_auto_20231024_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateexport',
            name='storage_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Код склада'),
        ),
        migrations.AlterField(
            model_name='templateexport',
            name='fields',
            field=apps.helpers.model_fields.ChoiceArrayField(base_field=models.CharField(choices=[('vendor_code', 'Код товара'), ('title', 'Наименование товара'), ('price', 'Цена товара'), ('product_group', 'Группа товара'), ('trademark', 'Торговая марка'), ('size', 'Размер'), ('color', 'Цвет'), ('barcode', 'Штрих-код'), ('barcode_x5', 'Штрих-код Х5'), ('data_matrix_code', 'Код DataMatrix'), ('zone_name', 'Наименование Зоны'), ('storage_code', 'Код склада'), ('counter_code', 'Код счетчика'), ('remainder_barcode', 'Остаток по штрихкоду'), ('box_number', 'Номер короба'), ('pallet_number', 'Номер паллеты'), ('count_scanned_product', 'Количество отсканированных товаров'), ('count', 'Количество'), ('zone_number', 'Номер зоны'), ('additional_product_name_1', 'Доп. наименование товара 1'), ('additional_product_name_2', 'Доп. наименование товара 2'), ('additional_product_name_3', 'Доп. наименование товара 3'), ('name_sk', 'Название по ШК'), ('name_sk_1', 'Название по ШК 1'), ('name_sk_2', 'Название по ШК 2'), ('name_sk_3', 'Название по ШК 3'), ('price_sk', 'Цена по ШК')], max_length=25, verbose_name='Поле'), size=None, verbose_name='Список полей'),
        ),
    ]
