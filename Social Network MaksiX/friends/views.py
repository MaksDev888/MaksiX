from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model

from friends.serializers import FriendsAPISerializer
from friends.services_friends import (
    get_user_pk,
    get_user_subscribers,
    delete_sub_relation,
    get_user_by_pk,
)
from permissions import IsActiveAndAuthenticated

user_model = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsActiveAndAuthenticated,
    ]
    serializer_class = FriendsAPISerializer

    def get_queryset(self) -> QuerySet:
        return get_user_subscribers(self.request.user)

    def create(self, request: Request) -> Response:
        if request.data.get("username") is None:
            return Response("Current user does not exists")
        else:
            request.data["from_user"] = get_user_pk(request.data["username"])
            request.data["to_user"] = request.user.pk
            serializer = FriendsAPISerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"You subscribed to": request.data["username"]}, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, pk: str) -> Response:
        from_user = get_user_by_pk(pk)
        delete_sub_relation(to_user=request.user, from_user=from_user)
        return Response("Unsubscribed")
