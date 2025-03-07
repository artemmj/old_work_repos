# Generated by Django 5.0.4 on 2024-08-23 07:13

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_news_options_newsemoji_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsRead',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, editable=False, null=True, verbose_name='Удален')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_read', to='news.news', verbose_name='Новость')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_read', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Просмотренная новость',
                'verbose_name_plural': 'Просмотренные новости',
            },
        ),
        migrations.AddConstraint(
            model_name='newsread',
            constraint=models.UniqueConstraint(fields=('news', 'user'), name='Просмотр новости пользователем'),
        ),
    ]
