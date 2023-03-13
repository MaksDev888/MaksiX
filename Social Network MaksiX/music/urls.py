from django.urls import path
from .views import *

urlpatterns = [
    path('album/', AlbumAPIList.as_view()),
    path('song/', SongAPIList.as_view()),
]