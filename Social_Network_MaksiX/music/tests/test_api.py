import json

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from knox.models import AuthToken

from music.models import Album, Song
from music.serializer import AlbumPostAPISerializer, SongSerializer
from music.services_music import get_album_list, get_own_list_album, get_own_list_song
from userdata.models import UserProfile


class MusicAPITestCase(APITestCase):
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
            is_activate=True,
        )

        self.album1 = Album.objects.create(
            name="album1",
        )
        self.album2 = Album.objects.create(
            name="album2",
        )
        self.album3 = Album.objects.create(
            name="album3",
        )
        self.song1 = Song.objects.create(
            name="Song1",
        )
        self.song2 = Song.objects.create(
            name="Song2",
        )
        self.album1.user.add(self.user1)
        self.album2.user.add(self.user1)

        self.song2.user.add(self.user1)
        self.song1.user.add(self.user1)

    @pytest.mark.django_db()
    def test_get_albums(self) -> None:
        url = reverse("album-list")
        self.authorization_user_by_token()
        response = self.client.get(url)
        albums = get_album_list()
        serializer = AlbumPostAPISerializer(albums, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    @pytest.mark.django_db()
    def test_get_my_albums(self) -> None:
        url = reverse("album-my-albums")
        self.authorization_user_by_token()
        response = self.client.get(url)
        albums = get_own_list_album(self.user1)
        serializer = AlbumPostAPISerializer(albums, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    @pytest.mark.django_db()
    def test_create_album(self) -> None:
        url = reverse("album-list")
        self.authorization_user_by_token()
        albums = get_own_list_song(self.user1).count()
        data = {
            "name": "album4",
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
        assert albums == get_own_list_song(self.user1).count()

    @pytest.mark.django_db()
    def test_delete_album(self) -> None:
        url = reverse("album-detail", kwargs={"pk": self.album1.id})
        self.authorization_user_by_token()
        albums = get_own_list_album(self.user1).count()
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert albums - 1 == get_own_list_album(self.user1).count()

    @pytest.mark.django_db()
    def test_get_list_song(self) -> None:
        url = reverse("song-list")
        self.authorization_user_by_token()
        response = self.client.get(url)
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    @pytest.mark.django_db()
    def test_get_list_user_song(self) -> None:
        url = reverse("song-my-songs")
        self.authorization_user_by_token()
        response = self.client.get(url)
        songs = get_own_list_song(self.user1)
        serializer = SongSerializer(songs, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    @pytest.mark.django_db()
    def test_delete_song_by_user(self) -> None:
        url = reverse("song-detail", kwargs={"pk": self.song1.id})
        self.authorization_user_by_token()
        user_song = get_own_list_song(self.user1).count()
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert user_song - 1 == get_own_list_song(self.user1).count()
