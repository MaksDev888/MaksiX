from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from knox.auth import TokenAuthentication



from userdata.models import UserProfile
from .serializers import *
from .models import Friend


try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


class UserAPIFriends(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):
        """ View the friends of a user """
        user = get_object_or_404(user_model, username=username)
        qs = Friend.objects.select_related("from_user").filter(to_user=user)
        username_list = []
        total = 0
        for i in qs:
            follower_username = str(i.from_user)
            username_list.append(follower_username)
            total += 1
        return Response(username_list, status=status.HTTP_200_OK)


class FollowAPIFriend(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [AllowAny, ]

    def post(self, request):
        from_user = str(UserProfile.objects.get(id=request.data.get('from_user')))
        serializer = FriendsAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'You subscribed to': from_user})


