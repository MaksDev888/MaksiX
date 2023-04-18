from django.urls import path, include
from rest_framework.routers import SimpleRouter, Route

from posts.views import PostViewSet


class CustomRouter(SimpleRouter):
    routes = [
        Route(
            url=r"^{prefix}/$",
            mapping={"get": "list", "post": "create"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        Route(
            url=r"^{prefix}\/(?P<user_pk>\d+)\/(?P<pk>\d+)\/$",
            mapping={"get": "retrieve"},
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Detail"},
        ),
        Route(
            url=r"^{prefix}\/(?P<user_pk>\d+)\/$",
            mapping={"get": "check_user_posts"},
            name="{basename}-user_posts",
            detail=False,
            initkwargs={"suffix": "Detail"},
        ),
    ]


router = CustomRouter()
router.register("post", PostViewSet, basename="post")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
