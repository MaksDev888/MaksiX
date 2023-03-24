from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')


urlpatterns = [
    path('api/v1/', include(router.urls)),
]