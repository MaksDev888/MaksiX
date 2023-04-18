from rest_framework import serializers

from friends.models import Friend


class FriendsAPISerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Friend:
        return Friend.objects.create(**validated_data)

    class Meta:
        model = Friend
        fields = ("from_user", "to_user")
