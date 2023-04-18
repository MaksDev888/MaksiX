from django.db.models import QuerySet

from userdata.models import UserProfile
from friends.models import Friend


def get_user_pk(username: str) -> int:
    return UserProfile.objects.get(username=username).pk


def get_user_by_pk(pk: str) -> UserProfile:
    return UserProfile.objects.get(pk=pk)


def get_user_subscribers(user: UserProfile) -> QuerySet:
    return Friend.objects.select_related("to_user").filter(from_user=user)


def delete_sub_relation(to_user: UserProfile, from_user: UserProfile) -> None:
    return Friend.objects.get(to_user=to_user, from_user=from_user).delete()
