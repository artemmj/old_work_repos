# Generated by Django 3.0.2 on 2022-03-31 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20220325_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='zone',
        ),
    ]
