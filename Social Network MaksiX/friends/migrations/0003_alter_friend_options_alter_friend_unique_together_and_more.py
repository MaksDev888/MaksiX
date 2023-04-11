# Generated by Django 4.1.6 on 2023-04-11 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("friends", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="friend",
            options={"verbose_name": "Subscribers", "verbose_name_plural": "Subscribers"},
        ),
        migrations.AlterUniqueTogether(
            name="friend",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="friend",
            name="from_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Получатель",
            ),
        ),
        migrations.AlterField(
            model_name="friend",
            name="to_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="friends",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Отправитель",
            ),
        ),
    ]
