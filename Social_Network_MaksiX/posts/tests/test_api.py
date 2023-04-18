import json

import pytest
from knox.models import AuthToken
from rest_framework import status

from posts.models import Posts
from posts.serializer import PostAPISerializer
from posts.services_posts import get_own_posts
from userdata.models import UserProfile
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse


class PostApiTestCase(APITestCase):
    def authorization_user_by_token(self) -> None:
        self.token = AuthToken.objects.create(self.user2)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token[1])

    def setUp(self) -> None:
        self.user1 = UserProfile.objects.create(
            password="examle1",
            username="user1",
            email="user1@mail.ru",
            full_name="user one",
            is_activate=True,
        )
        self.user2 = UserProfile.objects.create(
            password="examle2",
            username="user2",
            email="user2@mail.ru",
            full_name="user one",
            is_activate=True,
        )
        self.post1 = Posts.objects.create(
            owner=self.user1,
            title="post1",
            description="post1",
        )
        self.post2 = Posts.objects.create(
            owner=self.user2,
            title="post2",
            description="post2",
        )
        self.post3 = Posts.objects.create(
            owner=self.user2,
            title="post3",
            description="post3",
        )

    @pytest.mark.django_db()
    def test_get_request_user_posts(self) -> None:
        url = reverse("post-list")
        self.authorization_user_by_token()
        response = self.client.get(url)
        posts = get_own_posts(self.user2)
        serializer = PostAPISerializer(posts, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data
        assert len(response.data) == 2

    @pytest.mark.django_db()
    def test_get_random_user_post(self) -> None:
        url = reverse("post-user_posts", kwargs={"user_pk": self.user1.pk})
        self.authorization_user_by_token()
        response = self.client.get(url)
        posts = get_own_posts(self.user1)
        serializer = PostAPISerializer(posts, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    @pytest.mark.django_db()
    def test_detail_post(self) -> None:
        url = reverse("post-detail", kwargs={"pk": self.post1.pk, "user_pk": self.user1.pk})
        self.authorization_user_by_token()
        response = self.client.get(url)
        PostAPISerializer(self.post1)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_create_post(self) -> None:
        url = reverse("post-list")
        self.authorization_user_by_token()
        count_posts = Posts.objects.filter(owner=self.user2).count()
        data = {
            "title": "post4",
            "description": "post4",
        }
        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Posts.objects.filter(owner=self.user2).count() == count_posts + 1
