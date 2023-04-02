from userdata.models import UserProfile
from posts.models import Posts


def get_own_posts(user):
    return Posts.objects.filter(owner=user)


def get_user_by_pk(pk):
    return UserProfile.objects.get(pk=pk)


def get_all_posts(user):
    return Posts.objects.filter(owner=user)
