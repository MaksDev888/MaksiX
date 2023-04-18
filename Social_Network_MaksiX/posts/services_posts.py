from django.db.models import QuerySet

from userdata.models import UserProfile
from posts.models import Posts


def get_own_posts(user: UserProfile) -> QuerySet:
    return Posts.objects.filter(owner=user)


def get_user_by_pk(pk: str) -> UserProfile:
    return UserProfile.objects.get(pk=pk)


def get_all_user_posts(user: UserProfile) -> QuerySet:
    return Posts.objects.filter(owner=user)
