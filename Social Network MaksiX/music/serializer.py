from rest_framework import serializers
from rest_framework.serializers import BaseSerializer
from .models import *

from .models import *

class AlbumPostAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = '__all__'

class SongPostAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = '__all__'