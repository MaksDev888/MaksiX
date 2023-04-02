from rest_framework import serializers

from music.models import Album, Song


class AlbumPostAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("id", "name", "performer", "photo", "description")


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "name"]
