from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.services_posts import get_own_posts, get_user_by_pk, get_all_posts
from posts.serializer import PostAPISerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostAPISerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        self.queryset = get_own_posts(self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)

    @action(detail=True, methods=["get"], url_name="posts", url_path="posts")
    def check_user_post(self, request, pk=None):
        user = get_user_by_pk(pk)
        user_post = get_all_posts(user)
        serializer = PostAPISerializer(user_post, many=True)
        return Response(serializer.data)
