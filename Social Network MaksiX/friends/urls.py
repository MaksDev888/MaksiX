from django.urls import path, include
from .views import *

urlpatterns = [
    path('friends-list/<str:username>/', UserAPIFriends.as_view()),
    path('friend-request/', FollowAPIFriend.as_view()),
]