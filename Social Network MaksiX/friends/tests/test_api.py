import json

import pytest
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from friends.models import Friend
from friends.serializers import FriendsAPISerializer
from friends.services_friends import get_user_subscribers, delete_sub_relation
from userdata.models import UserProfile


class FollowingAPITestCase(APITestCase):
    def authorization_user_by_token(self) -> None:
        self.token = AuthToken.objects.create(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token[1])

    def setUp(self) -> None:
        self.user = UserProfile.objects.create_user(
            email="test_user@mail.ru", password="examle1", username="test_user", is_activate=True,
        )
        self.user2 = UserProfile.objects.create_user(
            email="test_user2@mail.ru", password="examle1", username="test_user1", is_activate=True,
        )
        self.user3 = UserProfile.objects.create_user(
            email="test_user3@mail.ru", password="examle1", username="test_user2", is_activate=True,
        )
        self.user4 = UserProfile.objects.create_user(
            email="test_user4@mail.ru", password="examle1", username="test_user3", is_activate=True,
        )

        Friend.objects.create(from_user=self.user, to_user=self.user2)
        Friend.objects.create(from_user=self.user, to_user=self.user3)


    @pytest.mark.django_db()
    def test_get_user_following(self) -> None:
        url = reverse("subscribers-list")
        self.authorization_user_by_token()
        response = self.client.get(url)
        following = get_user_subscribers(self.user)
        serializer = FriendsAPISerializer(following, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    @pytest.mark.django_db()
    def test_add_follower(self) -> None:
        url = reverse("subscribers-list")
        self.authorization_user_by_token()
        following = get_user_subscribers(self.user4).count()
        data = {
            "username": self.user4.username,
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type="application/json")
        following_new = get_user_subscribers(self.user4).count()
        assert response.status_code == status.HTTP_201_CREATED
        assert following + 1 == following_new

    @pytest.mark.django_db()
    def test_unfollowing_user(self) -> None:
        url = reverse("subscribers-detail", kwargs={"pk": self.user2.pk})
        Friend.objects.create(from_user=self.user2, to_user=self.user)
        self.authorization_user_by_token()
        following = get_user_subscribers(self.user2).count()
        delete_sub_relation(to_user=self.user2, from_user=self.user)
        response = self.client.delete(url)
        self.user.refresh_from_db()
        following_new = get_user_subscribers(self.user2).count()
        assert following - 1 == following_new
        assert response.status_code == status.HTTP_200_OK
