# Generated by Django 4.1.6 on 2023-03-13 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music.album', verbose_name='Альбом'),
        ),
    ]
