from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth import login

from knox import views as knox_views

from userdata.services import *
from userdata.serializers import (
    CreateUserSerializer,
    UpdateUserSerializer,
    LoginSerializer,
    UserSerializer,
    ShortUserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes_by_action = {
        "create": (AllowAny,),
        "update": (IsAuthenticated,),
        "partial_update": (IsAuthenticated,),
        "destroy": (IsAuthenticated,),
        "me": (IsAuthenticated,),
    }

    def get_queryset(self):
        self.queryset = get_all_user_list_without_yourself(self.request.user.pk)
        return self.queryset

    def get_serializer_class(
        self,
    ):
        if self.action in {"list", "retrieve"}:
            serializer = ShortUserSerializer
        else:
            serializer = UserSerializer
        return serializer

    def create(self, request, **kwargs):
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)

        if password == confirm_password:
            serializer = CreateUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(request.data)
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ""
            raise ValidationError(
                {"password_mismatch": "Password fields didnt not match."}
            )
        return Response(data, status=response)

    def update(self, request, pk):
        instance = request.user
        if instance.pk == int(pk):
            serializer = UpdateUserSerializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.validated_data, status=status.HTTP_205_RESET_CONTENT
            )

        response = status.HTTP_400_BAD_REQUEST
        return Response(
            "You are not authorized to perform this action", status=response
        )

    def partial_update(self, request, pk):
        """
        Переопределенный метод partial_update.
        Помимо частичного изменения модели, удаляет старую аватарку в случае ее передачи.
        :param request: Экземпляр класса Request DRF.
        :return:Responce DRF.
        """
        if request.user.pk == int(pk):
            try:
                request.data["avatar"] = request.FILES["image"]
                delete_old_avatar(request.user)
            except:
                pass
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "You are not authorized to perform this action",
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False)
    def me(self, request):
        """
        Возвращает данные о пользователе
        :param request:Экземпляр класса DRF
        :return:Responce DRF
        """
        user = request.user.pk
        serializer = self.get_serializer(get_user_by_pk(user))
        return Response(serializer.data)

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class LoginAPIView(knox_views.LoginView):
    """
    Класс представления выполняющий авторизацию пользователя.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(response.data, status=status.HTTP_200_OK)
