from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from permissions import IsActiveAndAuthenticated
from posts.models import Posts
from posts.services_posts import get_own_posts, get_user_by_pk, get_all_user_posts
from posts.serializer import PostAPISerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostAPISerializer
    permission_classes = [
        IsActiveAndAuthenticated,
    ]

    def get_queryset(self) -> QuerySet:
        self.queryset = get_own_posts(self.request.user)
        return self.queryset

    def retrieve(self, request: Request, pk: str, user_pk: str) -> Response:
        queryset = Posts.objects.all()
        post = get_object_or_404(queryset, pk=int(pk), owner=int(user_pk))
        serializer = PostAPISerializer(post)
        return Response(serializer.data)

    def perform_create(self, serializer: PostAPISerializer) -> None:
        serializer.save(owner=self.request.user)

    def check_user_posts(self, request: Request, user_pk: str) -> Response:
        user = get_user_by_pk(user_pk)
        user_post = get_all_user_posts(user)
        serializer = PostAPISerializer(user_post, many=True)
        return Response(serializer.data)
