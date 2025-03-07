# Generated by Django 3.0.2 on 2023-07-04 09:28

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0011_auto_20230623_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreparatoryInvitation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text='Пример, +79510549236', max_length=128, region=None, verbose_name='Номер телефона')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preparatory_invs', to='organization.Organization')),
            ],
            options={
                'verbose_name': 'Предварительное приглашение по номеру',
                'verbose_name_plural': 'Предварительные приглашения по номеру',
            },
        ),
        migrations.AddConstraint(
            model_name='preparatoryinvitation',
            constraint=models.UniqueConstraint(condition=models.Q(is_active=True), fields=('phone', 'organization'), name='unique_phone_org'),
        ),
    ]
