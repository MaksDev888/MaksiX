from django.urls import path, include
from rest_framework.routers import DefaultRouter

from knox.views import LogoutView, LogoutAllView

from .views import UserViewSet, LoginAPIView


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
]