from knox.auth import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from userdata.models import UserProfile
from .serializer import *
from .models import *

class AlbumAPIList(ListCreateAPIView):
    authentication_classes = [TokenAuthentication,]
    serializer_class = AlbumPostAPISerializer
    queryset = Album.objects.all()


    def post(self, request):
        request.data['performer'] = request.user.id
        serializer = AlbumPostAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data}, status=status.HTTP_200_OK)

class SongAPIList(APIView):
    authentication_classes = [TokenAuthentication,]

    def get(self, request):
        songs = Song.objects.all()
        serializer = SongPostAPISerializer(songs, many=True)

        return Response({'songs': serializer.data})


    def post(self, request):
        serializer = SongPostAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data}, status=status.HTTP_200_OK)


    def delete(self, request):
        user = request.user
        user.songs.remove(request.data['id'])
        return Response({'Song deleted'})