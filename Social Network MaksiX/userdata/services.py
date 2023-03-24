from environ import Path
import os

from .models import UserProfile


def get_user_by_pk(pk):
    return UserProfile.objects.get(pk=pk)


def check_created_email(email):
    return UserProfile.objects.filter(email=email).exists()


def delete_old_avatar(user):
    file_path = user.avatar
    print(file_path)
    os.remove(os.path.join(Path('media'), str(file_path)))
    return 'success'
