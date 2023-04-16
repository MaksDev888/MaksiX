import pytest
import json
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from userdata.models import UserProfile
from userdata.serializers import ShortUserSerializer, UserSerializer
from userdata.services import get_all_user_list_without_yourself


class UserApiTestCase(APITestCase):
    def authorization_user_by_token(self) -> None:
        self.token = AuthToken.objects.create(self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token[1])

    def setUp(self) -> None:
        self.user1 = UserProfile.objects.create(
            password="examle1",
            username="user1",
            email="user1@mail.ru",
            full_name="user one",
            bio="male",
            is_activate=True,
        )

        self.user2 = UserProfile.objects.create(
            password="examle2",
            username="user2",
            email="user2@mail.ru",
            full_name="user two",
            bio="male",
            is_activate=True,
        )
        self.user3 = UserProfile.objects.create(
            password="examle3",
            username="user3",
            email="user3@mail.ru",
            full_name="user three",
            bio="male",
            is_activate=True,
        )

    @pytest.mark.django_db()
    def test_get_all_user_without_yourself(self) -> None:
        url = reverse("user-list")
        self.authorization_user_by_token()
        response = self.client.get(url)
        users = get_all_user_list_without_yourself(pk=self.user1.pk)
        serializer = ShortUserSerializer(users, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data
        assert len(response.data) == 2

    @pytest.mark.django_db()
    def test_get_user_information(self) -> None:
        url = reverse("user-detail", kwargs={"pk": self.user1.pk})
        response = self.client.get(url)
        serializer = ShortUserSerializer(self.user1)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    @pytest.mark.django_db()
    def test_create_user(self) -> None:
        url = reverse("user-list")
        data = {
            "password": "examle4",
            "confirm_password": "examle4",
            "username": "user4",
            "email": "user4@mail.ru",
            "full_name": "user four",
            "bio": "male",
        }
        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == data["username"]

    @pytest.mark.django_db()
    def test_update_user(self) -> None:
        url = reverse("user-detail", kwargs={"pk": self.user1.pk})
        self.authorization_user_by_token()
        data = {"password": "examle5", "first_name": "userfive", "last_name": "sdfsad", "bio": "male"}
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type="application/json")
        assert response.status_code == status.HTTP_205_RESET_CONTENT
        assert response.data == data

    @pytest.mark.django_db()
    def test_change_avatar_by_partial_update(self) -> None:
        url = reverse("user-detail", kwargs={"pk": self.user1.pk})
        image_path = "userdata/tests/photo_for_test/test_img.jpeg"
        with open(image_path, "rb") as f:
            photo_stream = SimpleUploadedFile("photo.jpg", f.read(), content_type="image/jpeg")
        data = {"avatar": photo_stream}
        self.authorization_user_by_token()
        response = self.client.patch(url, data, format="multipart")
        assert response.status_code == status.HTTP_205_RESET_CONTENT
        self.user1.refresh_from_db()
        assert self.user1.avatar is not None

    @pytest.mark.django_db()
    def test_check_yourself_information(self) -> None:
        url = reverse("user-me")
        self.authorization_user_by_token()
        response = self.client.get(url)
        user = UserProfile.objects.get(pk=self.user1.pk)
        serializer = UserSerializer(user)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    @pytest.mark.django_db()
    def test_login(self) -> None:
        url = reverse("user-login")
        data = {
            "password": "examle1",
            "email": "user1@mail.ru",
        }
        self.client.post(url, data, format="json")
        assert self.user1.is_authenticated is True
