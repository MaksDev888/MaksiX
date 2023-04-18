from django.contrib.auth import authenticate
from rest_framework import serializers

from userdata.models import UserProfile
from userdata.services import check_created_email


class UserSerializer(serializers.ModelSerializer):
    """
    Серелизатор пользователя.
    """

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "years_old",
            "address",
            "avatar",
            "full_name",
        )


class ShortUserSerializer(serializers.ModelSerializer):
    """
    Серелизатор для просмотра пользовательских данных.
    """

    class Meta:
        model = UserProfile
        fields = ("id", "full_name", "username", "bio")


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Серелизатор для создания пользователя.
    """

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "years_old",
            "address",
            "avatar",
            "full_name",
            "password",
            "confirm_password",
        )

    def validate(self, attrs: dict) -> dict:
        """
        Валидация email и его проверка на существование в БД.
        :param: JSON Request.
        :return: Валидный email.
        """
        email = attrs.get("email", "").strip().lower()

        if check_created_email(email):
            raise serializers.ValidationError("User with this email id already exists.")

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if not password or not confirm_password:
            raise serializers.ValidationError("Password and confirm_password are required.")
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm_password should be equal.")
        attrs.pop("confirm_password")
        return attrs

    def create(self, validated_data: dict) -> UserProfile:
        """
        Метод создания модели пользователя.
        :param validated_data: Валидные данные.
        :return: Модель User.
        """
        return UserProfile.objects.create_user(**validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Серелизатор для полного или частичного обновления модели.
    """

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    bio = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "bio", "password", "avatar")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_pk(self, pk: str) -> str:
        """
        Метод для проверки переданного pk и user.pk
        :param value: Первичный ключ.
        :return: Валидный первичный ключ.
        """
        if int(pk) != self.instance.pk:
            raise serializers.ValidationError("You cannot change this user.")
        return pk

    def update(self, instance: object, validated_data: dict) -> UserProfile:
        """
        Метод сохранящий данные и вызывающий сохранение зашифрованого пароля в БД.
        :param instance: UserProfile
        :param validated_data: Валидные данные.
        :return: Обновлённая модель UserProfile.
        """
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Серелизатор для авторизаии пользователя.
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs: dict) -> dict:
        """
        Метод не позволяющий авторизоваться по несуществующим данным.
        :param: email, password.
        :return: Модель User.
        """
        email = attrs.get("email").lower()
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password.")

        if not check_created_email(email):
            raise serializers.ValidationError("Email does not exist.")

        user = authenticate(request=self.context.get("request"), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs["user"] = user
        return attrs
