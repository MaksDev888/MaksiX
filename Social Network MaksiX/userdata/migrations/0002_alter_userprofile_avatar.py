# Generated by Django 4.1.6 on 2023-03-19 14:16

from django.db import migrations, models
import userdata.models


class Migration(migrations.Migration):
    dependencies = [
        ("userdata", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=userdata.models.user_directory_path,
                verbose_name="Изображение страницы",
            ),
        ),
    ]
