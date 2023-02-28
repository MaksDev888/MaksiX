from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core import serializers

from .serializers import *
from .models import Friend
from userdata.serializers import UserSerializer


try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


class UserAPIFriends(APIView):
    serializer_class = FriendsAPISerializer
    permission_classes = (AllowAny,)

    def get(self, request, username):
        """ View the friends of a user """
        user = get_object_or_404(user_model, username=username)
        qs = Friend.objects.select_related("from_user").filter(to_user=user)
        print(qs)
        friends = FriendsAPISerializer(qs)
        friends_list = FriendsAPISerializer(data=friends.data)
        print(friends)
        print(friends_list)
        print(type(friends))

        # serializer_user = UserSerializer(user)
        # serializer_user_valid = UserSimpleSerializer(data=serializer_user.data)
        # serializer_user_valid.is_valid()
        # print(serializer_user_valid.errors)
        # friends = Friend.objects.friends(user=serializer_user.data)
        return Response(friends, status=status.HTTP_200_OK)



