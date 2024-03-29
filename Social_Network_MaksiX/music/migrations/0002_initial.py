# Generated by Django 4.1.6 on 2023-03-16 18:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("music", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="song",
            name="user",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name="пользователь"),
        ),
        migrations.AddField(
            model_name="album",
            name="user",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name="Пользвователь"),
        ),
    ]
