from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request


class IsActiveAndAuthenticated(IsAuthenticated):
    def has_permission(self, request: Request, view: object) -> bool:
        is_authenticated = super().has_permission(request, view)
        is_active = request.user.is_activate
        return is_authenticated and is_active
