from rest_framework import serializers

from .models import Friend


class FriendsApiList(serializers.Serializer):
    from_user = serializers.CharField()


class FriendsAPISerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Friend.objects.create(**validated_data)

    class Meta:
        model = Friend
        fields = '__all__'


