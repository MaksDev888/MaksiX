from rest_framework import serializers

from .models import *


class AlbumPostAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = '__all__'


class SongPostAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id','name']