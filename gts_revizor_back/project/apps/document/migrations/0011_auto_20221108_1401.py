# Generated by Django 3.0.2 on 2022-11-08 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_remove_task_document'),
        ('document', '0010_auto_20221103_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='auditor_scan_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auditor_scan_document', to='task.Task'),
        ),
        migrations.AddField(
            model_name='document',
            name='counter_scan_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counter_scan_document', to='task.Task'),
        ),
    ]
