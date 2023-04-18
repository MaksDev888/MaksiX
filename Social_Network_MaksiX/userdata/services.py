from django.db.models import QuerySet
from environ import Path
import os

from userdata.models import UserProfile


def get_all_user_list_without_yourself(pk: int) -> QuerySet:
    """
    Получение списка всех юзеров, юзера который отправляет запрос.
    """
    UserProfile.objects.exclude(pk=pk)
    return UserProfile.objects.exclude(pk=pk)


def get_user_by_pk(pk: int) -> UserProfile:
    """
    Получение user по pk.
    """
    return UserProfile.objects.get(pk=pk)


def check_created_email(email: str) -> bool:
    """
    Проверка на существование email в БД.
    """
    return UserProfile.objects.filter(email=email).exists()


def delete_old_avatar(user: UserProfile) -> str:
    """
    Удаление предыдущей аватарки при загрузке новой.
    """
    file_path = user.avatar
    os.remove(os.path.join(Path("media"), str(file_path)))
    return "success"
