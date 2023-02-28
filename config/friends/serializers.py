from rest_framework import serializers

from .models import *

class FriendsAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Friend
        fields = '__all__'

# class NameAPISerializer(serializers.Serializer):
#     class Meta:
#     username = serializers.CharField(max_length=200)