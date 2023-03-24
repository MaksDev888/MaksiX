from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth import login

from knox import views as knox_views

from .services import *
from .serializers import CreateUserSerializer, UpdateUserSerializer, LoginSerializer, UserSerializer, \
    ShortUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        queryset = UserProfile.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        user = request.user
        if user.pk == int(pk):
            serializer = UserSerializer(get_user_by_pk(pk))
            return Response(serializer.data)

        serializer = ShortUserSerializer(get_user_by_pk(pk))
        return Response(serializer.data)

    def create(self, request, **kwargs):
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        if password == confirm_password:
            serializer = CreateUserSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ''
            raise ValidationError({
                'password_mismatch': 'Password fields didnt not match.'
            })
        return Response(data, status=response)

    def put(self, request):
        instance = request.user
        serializer = UpdateUserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data)

    def patch(self, request):
        try:
            request.data['avatar'] = request.FILES['image']
            delete_old_avatar(request.user)
        except:
            pass
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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






