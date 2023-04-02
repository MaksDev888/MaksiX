from django.urls import path, include
from rest_framework import routers

from friends.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"subscribers", UserViewSet, basename="subscribers")

urlpatterns = [
    path("", include(router.urls)),
]
