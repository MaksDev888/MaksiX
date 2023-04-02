from django.contrib import admin
from music.models import Album, Song


class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "performer", "description")


class SongAdmin(admin.ModelAdmin):
    list_display = ("name", "artist", "album")


admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
