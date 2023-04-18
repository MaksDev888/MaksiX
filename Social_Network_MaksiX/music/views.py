from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets

from music.serializer import AlbumPostAPISerializer, SongSerializer
from music.services_music import (
    get_song_list,
    get_own_list_song,
    delete_song,
    get_album_list,
    get_own_list_album,
    delete_album,
)
from permissions import IsActiveAndAuthenticated


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = get_album_list()
    serializer_class = AlbumPostAPISerializer
    permission_classes = [
        IsActiveAndAuthenticated,
    ]

    def perform_create(self, serializer: AlbumPostAPISerializer) -> None:
        instance = serializer.save(performer=self.request.user.id)
        instance.user.add(self.request.user)

    def destroy(self, request: Request, pk: str) -> Response:
        return delete_album(user=request.user, album_id=pk)

    @action(detail=False, methods=["get"])
    def my_albums(self, request: Request) -> Response:
        user_album = get_own_list_album(request.user)
        serializer = AlbumPostAPISerializer(user_album, many=True)
        return Response(serializer.data)


class SongViewSet(viewsets.ModelViewSet):
    queryset = get_song_list()
    serializer_class = SongSerializer
    permission_classes = [
        IsActiveAndAuthenticated,
    ]

    def destroy(self, request: Request, pk: str) -> Response:
        return delete_song(user=request.user, song_id=pk)

    @action(detail=False, methods=["get"])
    def my_songs(self, request: Request) -> Response:
        user_songs = get_own_list_song(request.user)
        serializer = SongSerializer(user_songs, many=True)
        return Response(serializer.data)
