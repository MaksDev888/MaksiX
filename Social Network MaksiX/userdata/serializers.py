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
        fields = ("full_name", "username", "bio")


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Серелизатор для создания пользователя.
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
            "password",
        )
        extra_kwargs = {"password": {"required": True}}

    def validate(self, attrs):
        """
        Валидация email и его проверка на существование в БД.
        :param: JSON Request.
        :return: Валидный email.
        """
        email = attrs.get("email", "").strip().lower()
        if check_created_email(email):
            raise serializers.ValidationError("User with this email id already exists.")
        return attrs

    def create(self, validated_data):
        """
        Метод создания модели пользователя.
        :param validated_data: Валидные данные.
        :return: Модель User.
        """
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Серелизатор для полного или частичного обновления модели.
    """

    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "bio", "password", "avatar")

    def update(self, instance, validated_data):
        """
        Метод сохранящий данные и вызывающий сохранение зашифрованого пароля в БД.
        :param validated_data: Валидные данные.
        :return: Обновлённая модель User.
        """
        password = validated_data.pop("password")
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


class LoginSerializer(serializers.Serializer):
    """
    Серелизатор для авторизаии пользователя.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
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

        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs["user"] = user
        return attrs
