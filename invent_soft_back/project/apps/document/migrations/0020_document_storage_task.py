# Generated by Django 3.0.2 on 2023-11-21 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_auto_20231030_1512'),
        ('document', '0019_auto_20231025_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='storage_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='storage_document', to='task.Task'),
        ),
    ]
