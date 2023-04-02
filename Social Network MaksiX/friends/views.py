from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from friends.serializers import FriendsAPISerializer
from friends.services_friends import (
    get_user_pk,
    get_user_subscribers,
    delete_sub_relation,
)

user_model = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = FriendsAPISerializer

    def get_queryset(self):
        queryset = get_user_subscribers(self.request.user)
        return queryset

    def create(self, request):
        if request.data.get("username") == None:
            return Response("Current user does not exists")
        else:
            request.data["from_user"] = get_user_pk(request.data["username"])
            request.data["to_user"] = request.user.pk
            serializer = FriendsAPISerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"You subscribed to": request.data["username"]})

    def destroy(self, request, pk=None):
        delete_sub_relation(request.user, from_user=pk)
        return Response("Unsubscribed")
