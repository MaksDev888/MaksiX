from django.contrib.auth.base_user import BaseUserManager

from PIL import Image


MAX_THUMBNAIL_SIZE = 200


class UserManager(BaseUserManager):
    """
    Менеджер для создания user и superuser.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Метод обрабатывающий email, вызывает шифрование password.
        :param: validate_data.
        :return: Модель user.
        """
        if not email:
            raise ValueError("The email is not given.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Метод добавляющий superuser дефолтные поля.
        :param validate_data: Валидные данные.
        :return: Модель superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(email, password, **extra_fields)

    def resize_logo(instance):
        """
        Изменение размеров логотипа при большом размере изображения.
        """
        width = instance.avatar.width
        height = instance.avatar.height

        filename = instance.avatar.path

        max_size = max(width, height)

        if max_size > MAX_THUMBNAIL_SIZE:
            image = Image.open(filename)
            image = image.resize(
                (
                    round(width / max_size * MAX_THUMBNAIL_SIZE),
                    round(height / max_size * MAX_THUMBNAIL_SIZE),
                ),
                Image.ANTIALIAS,
            )
            image.save(filename)
