from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"guilds", views.GuildViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("langs/", views.langs),
    path("health/", views.health_check),
    path("events/", views.events),
]
