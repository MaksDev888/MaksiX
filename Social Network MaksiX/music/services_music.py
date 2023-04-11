from django.db.models import QuerySet
from rest_framework.response import Response

from music.models import Song, Album
from userdata.models import UserProfile


def get_user_song(user: UserProfile) -> Song:
    return user.songs.all()


def delete_song(user: UserProfile, song_id: str) -> Response:
    try:
        Song.objects.get(id=song_id)
    except Song.DoesNotExist:
        return Response("Song does not exist")
    else:
        user.songs.remove(song_id)
        return Response("Song deleted")


def delete_album(user: UserProfile, album_id: str) -> Response:
    try:
        Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        return Response("Album does not exist")
    else:
        user.album_set.remove(album_id)
        return Response("Album deleted")


def get_song_list() -> QuerySet:
    return Song.objects.all()


def get_own_list_song(user: UserProfile) -> QuerySet:
    return Song.objects.filter(user=user)


def get_own_list_album(user: UserProfile) -> QuerySet:
    return Album.objects.filter(user=user)


def get_album_list() -> QuerySet:
    return Album.objects.all()
