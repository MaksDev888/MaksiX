from django.urls import path, include
from knox.views import LogoutView, LogoutAllView
from .views import *

urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('update-user/<int:pk>/', UpdateUserAPI.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('list_songs/', SongAPIList.as_view()),
]