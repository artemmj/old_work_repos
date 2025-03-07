# Generated by Django 3.0.2 on 2022-05-11 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20220511_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='am',
            field=models.CharField(blank=True, choices=[('without_verification_am', 'Без проверки АМ'), ('only_presence_am', 'Только наличие АМ'), ('conformity_am_shk', 'Соответствие АМ и ШК')], max_length=23, null=True, verbose_name='Акцизная марка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='dm',
            field=models.CharField(blank=True, choices=[('without_verification_dm', 'Без проверки ДМ'), ('only_presence_dm', 'Только наличие ДМ'), ('conformity_dm_shk', 'Соответствие ДМ и ШК')], max_length=23, null=True, verbose_name='Датаматрикс'),
        ),
    ]
