from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializer import *
from .services_music import\
    get_songs,\
    get_own_list_song,\
    delete_song,\
    get_album_list,\
    get_own_list_album


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = get_album_list()
    serializer_class = AlbumPostAPISerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        request.data['performer'] = request.user.id
        serializer = AlbumPostAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def user_albums(self, request):
        user_album = get_own_list_album(request.user)
        serializer = AlbumPostAPISerializer(user_album, many=True)

        return Response(serializer.data)


class SongViewSet(viewsets.ModelViewSet):
    queryset = get_songs()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated, ]

    def destroy(self, request, pk):
        return delete_song(user=request.user, song_id=pk)

    @action(detail=False, methods=['get'])
    def user_songs(self, request):
        user_songs = get_own_list_song(request.user)
        serializer = SongSerializer(user_songs, many=True)
        return Response(serializer.data)