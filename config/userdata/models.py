from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

def user_directory_path(instance, filename):
    """Функция создающая путь куда осуществляться загрузка MEDIA_ROOT/user_<id>/<filename> для Profile"""
    return 'user_{0}/images/{1}'.format(instance.user.id, filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email is not given.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    GENDER = [
        ('male', 'мужской'),
        ('female', 'Женский'),
    ]
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    avatar = models.ImageField(upload_to=user_directory_path, verbose_name='Изображение страницы',blank=True, null = True,
                               default='https://img1.goodfon.ru/original/800x480/4/a3/kot-britanskiy-britanec-seryy.jpg')
    bio = models.CharField(max_length=7, choices=GENDER)
    years_old = models.IntegerField(verbose_name='Возраст', blank=True,null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True, null = True)

    class Meta:
        verbose_name = 'Данные пользователя'
        verbose_name_plural = 'Данные пользователя'


    def __str__(self):
        return self.username








