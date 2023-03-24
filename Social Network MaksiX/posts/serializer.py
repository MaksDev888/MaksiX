from rest_framework import serializers

from .models import Posts


class PostAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = '__all__'