from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView

from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'full_name','username', 'bio')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if UserProfile.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists.')
        return attrs

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'bio', 'password')

    def update(self, instance, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        print(validated_data)
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password.")

        if not UserProfile.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email,
                            password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs


