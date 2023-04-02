from rest_framework import serializers

from friends.models import Friend


class FriendsAPISerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source="from_user.username")

    def create(self, validated_data):
        return Friend.objects.create(**validated_data)

    class Meta:
        model = Friend
        fields = ("from_user",)
