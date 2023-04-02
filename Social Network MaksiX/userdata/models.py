from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from userdata.managers import UserManager


def user_directory_path(instance, filename):
    """Функция создающая путь куда осуществляться загрузка MEDIA_ROOT/user_<id>/<filename> для Profile"""
    return "user_{0}/avatar/{1}".format(instance.id, filename)


class UserProfile(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    GENDER = [
        ("male", "мужской"),
        ("female", "Женский"),
    ]
    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    avatar = models.ImageField(
        upload_to=user_directory_path,
        verbose_name="Изображение страницы",
        blank=True,
        null=True,
    )
    bio = models.CharField(max_length=7, choices=GENDER)
    years_old = models.IntegerField(verbose_name="Возраст", blank=True, null=True)
    address = models.CharField(
        max_length=255, verbose_name="Адрес", blank=True, null=True
    )

    objects = UserManager()

    class Meta:
        verbose_name = "Данные пользователя"
        verbose_name_plural = "Данные пользователя"

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        if self.avatar:
            UserManager.resize_logo(self)

    def __str__(self):
        return self.username
