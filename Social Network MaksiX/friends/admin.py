from django.contrib import admin
from .models import Friend


class FriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_user', 'from_user')


admin.site.register(Friend, FriendAdmin)