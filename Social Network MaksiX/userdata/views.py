from django.core.mail import send_mail
from django.db.models import QuerySet
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from django.core.signing import Signer
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth import login

from knox import views as knox_views
from rest_framework.views import APIView

from config import settings
from permissions import IsActiveAndAuthenticated
from userdata.models import UserProfile
from userdata.services import get_all_user_list_without_yourself, delete_old_avatar, get_user_by_pk
from userdata.serializers import (
    CreateUserSerializer,
    UpdateUserSerializer,
    LoginSerializer,
    UserSerializer,
    ShortUserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsActiveAndAuthenticated,)
    parser_classes = [MultiPartParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ["id"]
    search_fields = ["id", "username"]

    permission_classes_by_action = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "create": (AllowAny,),
        "update": (IsActiveAndAuthenticated,),
        "partial_update": (IsActiveAndAuthenticated,),
        "destroy": (IsActiveAndAuthenticated,),
        "me": (IsActiveAndAuthenticated,),
    }

    def get_queryset(self) -> QuerySet:
        self.queryset = get_all_user_list_without_yourself(self.request.user.pk)
        return self.queryset

    def get_serializer_class(
        self,
    ) -> type[UserSerializer | CreateUserSerializer | UpdateUserSerializer]:
        if self.action in {"list", "retrieve"}:
            serializer = ShortUserSerializer
        elif self.action == "create":
            serializer = CreateUserSerializer
        else:
            serializer = UserSerializer
        return serializer

    def update(self, request: list, pk: str) -> Response:
        user = request.user
        serializer = UpdateUserSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("pk", None)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_205_RESET_CONTENT)

    def partial_update(self, request: Request, pk: str) -> Response:
        """
        Переопределенный метод partial_update.
        Помимо частичного изменения модели, удаляет старую аватарку в случае ее передачи.
        :param request: Экземпляр класса Request DRF.
        :return:Responce DRF.
        """
        if request.user.pk == int(pk):
            try:
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
    def me(self, request: Request) -> Response:
        """
        Возвращает данные о пользователе
        :param request:Экземпляр класса DRF
        :return:Responce DRF
        """
        user = request.user.pk
        serializer = self.get_serializer(get_user_by_pk(user))
        return Response(serializer.data)

    def get_permissions(self) -> list:
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class LoginAPIView(knox_views.LoginView):
    """
    Класс представления выполняющий авторизацию пользователя.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)


class ConfirmEmailView(APIView):
    def post(self, request: Request) -> Response:
        email = request.user.email
        user = UserProfile.objects.get(email=email)

        if not user.is_activate:
            signer = Signer()
            encrypted_email = signer.sign(email)
            link = f"http://127.0.0.1:8000{reverse('email_confirmation')}?email={encrypted_email}"
            send_mail(
                "Confirm your email",
                link,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"detail": "The email has already been confirmed."}, status=status.HTTP_400_BAD_REQUEST)


class EmailConfirmationView(APIView):
    def post(self, request: Request) -> Response:
        email = request.user.email
        encrypted_email = request.GET.get("email")
        signer = Signer()
        user_encrypted_email = signer.sign(email)
        if user_encrypted_email == encrypted_email:
            try:
                user = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                return Response({"detail": "User with provided email not found."}, status=status.HTTP_404_NOT_FOUND)
            if user.is_activate:
                return Response({"detail": "Email is already confirmed."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.is_activate = True
                user.save()
                return Response({"detail": "Email confirmed successfully."}, status=status.HTTP_200_OK)
