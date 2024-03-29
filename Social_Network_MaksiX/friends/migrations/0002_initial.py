# Generated by Django 4.1.6 on 2023-03-16 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("friends", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="friend",
            name="from_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="_unused_friend_relation",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="friend",
            name="to_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="friends",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="friend",
            unique_together={("from_user", "to_user")},
        ),
    ]
