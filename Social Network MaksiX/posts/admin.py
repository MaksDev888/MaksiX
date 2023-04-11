from django.contrib import admin

from posts.models import Posts


class PostsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner")
    list_display_links = ("title",)
    search_fields = ("title", "id", "owner")


admin.site.register(Posts, PostsAdmin)
