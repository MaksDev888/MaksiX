from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services_posts import get_own_posts, get_user_by_pk, get_all_posts
from .serializer import PostAPISerializer


class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        qs = get_own_posts(request.user)
        serializer = PostAPISerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['owner'] = request.user.id
        serializer = PostAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    @action(detail=True, methods=['get'], url_name='look_post', url_path='look-post')
    def check_user_post(self, request, pk=None):
        user = get_user_by_pk(pk)
        user_post = get_all_posts(user)
        serializer = PostAPISerializer(user_post, many=True)
        return Response(serializer.data)