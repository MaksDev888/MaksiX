from django.db import models

from config.settings import AUTH_USER_MODEL

def user_directory_path_for_album_image(instance, filename):
    """Функция создающая путь куда осуществляется загрузка MEDIA_ROOT/user_<id>/posts_images/<filename> для Posts"""
    return 'album_images/{0}'.format(filename)

def user_directory_path_for_song_image(instance, filename):
    """Функция создающая путь куда осуществляется загрузка MEDIA_ROOT/user_<id>/posts_images/<filename> для Posts"""
    return 'song/song_images/{0}'.format(filename)


class Album(models.Model):
    name = models.CharField(max_length=255)
    performer = models.CharField(max_length=255, verbose_name='Исполнитель', blank=True)
    photo = models.ImageField(upload_to=user_directory_path_for_album_image, verbose_name='Фото альбома', blank=True)
    description = models.CharField(max_length=700, blank=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название песни')
    artist = models.CharField(max_length=255, verbose_name='Исполнитель')
    photo = models.ImageField(upload_to=user_directory_path_for_song_image, verbose_name='Фото песни', blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='Альбом',blank=True, null=True)

    def __str__(self):
        return self.name