from rest_framework.response import Response

from .models import Song, Album


def get_user_song(user):
    return user.songs.all()


def delete_song(user, song_id):
    try:
        Song.objects.get(id=song_id)
    except Song.DoesNotExist:
        return Response('Song does not exist')
    else:
        user.songs.remove(song_id)
        return Response('Song deleted')


def get_songs():
    return Song.objects.all()


def get_own_list_song(user):
    return Song.objects.filter(user=user)


def get_own_list_album(user):
    return Album.objects.filter(user=user)


def get_album_list():
    return Album.objects.all()