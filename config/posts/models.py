# from django.db import models
# from django.contrib.auth.models import User
#
# def user_directory_path_for_post_image(instance, filename):
#     """Функция создающая путь куда осуществляется загрузка MEDIA_ROOT/user_<id>/posts_images/<filename> для Posts"""
#     return 'user_{0}/posts_images/{1}'.format(instance.user_id, filename)
#
# class Posts(models.Model):
#     title = models.CharField(max_length=50, verbose_name='Название')
#     description = models.CharField(max_length=400, verbose_name='Описание')
#     post_image = models.ImageField(upload_to=user_directory_path_for_post_image, verbose_name='Изображение поста')
#     created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
