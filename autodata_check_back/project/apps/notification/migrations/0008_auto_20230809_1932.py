# Generated by Django 3.0.2 on 2023-08-09 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_task', '0014_auto_20230801_1504'),
        ('notification', '0007_auto_20230808_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskFixOrganizationInspectorNotification',
            fields=[
                ('basenotification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification.BaseNotification')),
                ('inspection_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_fix_organization_inspector_notifications', to='inspection_task.InspectionTask', verbose_name='Задание на осмотр')),
            ],
            options={
                'verbose_name': 'Уведомление о правках в задании инспектору организации',
                'verbose_name_plural': 'Уведомления о правках в задании инспектору организации',
                'ordering': ('-created_at',),
            },
            bases=('notification.basenotification',),
        ),
        migrations.CreateModel(
            name='TaskFixServiceInspectorNotification',
            fields=[
                ('basenotification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification.BaseNotification')),
                ('inspection_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_fix_service_inspector_notifications', to='inspection_task.InspectionTask', verbose_name='Задание на осмотр')),
            ],
            options={
                'verbose_name': 'Уведомление о правках в задании инспектору сервиса',
                'verbose_name_plural': 'Уведомления о правках в задании инспектору сервиса',
                'ordering': ('-created_at',),
            },
            bases=('notification.basenotification',),
        ),
        migrations.DeleteModel(
            name='TaskFixNotification',
        ),
    ]
