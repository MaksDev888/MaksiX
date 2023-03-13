from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView
from knox.auth import TokenAuthentication
from rest_framework.response import Response

from userdata.models import UserProfile
from .models import *
from .serializer import *

class PostAPIList(ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    serializer_class = PostAPISerializer

    def get(self, request):
        qs = Posts.objects.filter(owner=request.user)
        serializer = PostAPISerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['owner']=request.user.id
        serializer = PostAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

