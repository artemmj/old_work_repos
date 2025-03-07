# Generated by Django 3.0.2 on 2023-04-13 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0015_auto_20230413_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='sign_client',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='sign_inspector',
        ),
        migrations.AddField(
            model_name='signclient',
            name='inspection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='signs_client', to='inspection.Inspection', verbose_name='Осмотр'),
        ),
        migrations.AddField(
            model_name='signinspector',
            name='inspection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='signs_inspector', to='inspection.Inspection', verbose_name='Осмотр'),
        ),
    ]
