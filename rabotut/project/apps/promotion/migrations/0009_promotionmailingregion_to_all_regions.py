# Generated by Django 5.0.4 on 2024-10-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0008_alter_basepromotionmailing_publish_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionmailingregion',
            name='to_all_regions',
            field=models.BooleanField(blank=True, null=True, verbose_name='Рассылка на все регионы'),
        ),
    ]
