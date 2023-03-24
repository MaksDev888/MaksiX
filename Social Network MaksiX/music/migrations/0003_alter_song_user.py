# Generated by Django 4.1.6 on 2023-03-19 14:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='songs', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
