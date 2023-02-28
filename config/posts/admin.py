# from django.contrib import admin
#
# from django.contrib import admin
# from .models import Posts
#
# class Post_admin(admin.ModelAdmin):
#
#     def save_model(self, request, obj, form, change):
#         in not obj.created_by_id:
#             obj.created_by_id = request.user
#         obj.save()
#
#
# admin.site.register(Posts, Post_admin)