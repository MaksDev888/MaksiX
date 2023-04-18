from rest_framework import serializers

from posts.models import Posts


class PostAPISerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Posts
        fields = ("id", "title", "description", "post_image", "owner")
