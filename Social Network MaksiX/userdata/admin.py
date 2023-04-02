from django.contrib import admin

from userdata.models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "full_name", "avatar", "years_old")
    list_display_links = ("full_name", "username")
    search_fields = ("title", "full_name", "username")


admin.site.register(UserProfile, ProfileAdmin)
