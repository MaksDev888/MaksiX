from userdata.models import UserProfile
from friends.models import Friend


def get_user_pk(username):
    return UserProfile.objects.get(username=username).pk


def get_user_subscribers(user):
    return Friend.objects.select_related("from_user").filter(to_user=user)


def delete_sub_relation(user, from_user):
    return Friend.objects.filter(to_user=user, from_user=from_user).delete()
