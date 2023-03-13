from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import CreateUserSerializer, UpdateUserSerializer, LoginSerializer
from knox import views as knox_views
from django.contrib.auth import login



class CreateUserAPI(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UpdateUserAPI(UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UpdateUserSerializer


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)

class SongAPIList(ListAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)

        return Response({'songs':user.albums})
