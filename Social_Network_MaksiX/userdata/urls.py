from django.urls import path, include
from rest_framework.routers import DefaultRouter

from knox.views import LogoutView, LogoutAllView


from userdata.views import UserViewSet, LoginAPIView, ConfirmEmailView, EmailConfirmationView

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")


urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("login/", LoginAPIView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view()),
    path("logout-all/", LogoutAllView.as_view()),
    path("confirm-email/", ConfirmEmailView.as_view(), name="confirm_email"),
    path("email-confirmation/", EmailConfirmationView.as_view(), name="email_confirmation"),
]
