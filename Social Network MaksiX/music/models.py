from django.db import models

from userdata.models import UserProfile


def user_directory_path_for_album_image(filename: str) -> str:
    """Функция создающая путь куда осуществляется загрузка MEDIA_ROOT/user_<id>/posts_images/<filename> для Posts"""
    return f"album_images/{filename}"


def user_directory_path_for_song_image(filename: str) -> str:
    """Функция создающая путь куда осуществляется загрузка MEDIA_ROOT/user_<id>/posts_images/<filename> для Posts"""
    return f"song/song_images/{filename}"


class Album(models.Model):
    name = models.CharField(max_length=255)
    performer = models.CharField(max_length=255, verbose_name="Исполнитель", blank=True)
    photo = models.ImageField(
        upload_to=user_directory_path_for_album_image,
        verbose_name="Фото альбома",
        blank=True,
    )
    description = models.CharField(max_length=700, blank=True)
    user = models.ManyToManyField(UserProfile, verbose_name="Пользвователь", blank=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название песни")
    artist = models.CharField(max_length=255, verbose_name="Исполнитель")
    photo = models.ImageField(
        upload_to=user_directory_path_for_song_image,
        verbose_name="Фото песни",
        blank=True,
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name="Альбом", blank=True, null=True)
    user = models.ManyToManyField(UserProfile, verbose_name="пользователь", blank=True, related_name="songs")

    objects = None

    def __str__(self):
        return self.name
