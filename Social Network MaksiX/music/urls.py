from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AlbumViewSet, SongViewSet


router = DefaultRouter()
router.register(r'album', AlbumViewSet)
router.register(r'song', SongViewSet)


urlpatterns = [
    path('', include(router.urls)),
]