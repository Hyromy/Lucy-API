from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import models, serializers
from .gossiper import publish_on_redis, redis_payload, event_name


class GuildViewSet(viewsets.ModelViewSet):
    queryset = models.Guild.objects.all()
    serializer_class = serializers.GuildSerializer

    def _redis_payload_keys(self, event: str, instance: models.Guild, /) -> dict:
        return {
            "event": event,
            "version": instance.version,
            "updated_at": instance.updated_at.isoformat(),
            "source": self.request.headers.get("X-Source", "api request"),
        }

    def perform_update(self, serializer: serializers.GuildSerializer):
        instance: models.Guild = serializer.save()
        instance.version += 1
        instance.save(update_fields=["version"])

        event = event_name("guild", "updated")
        publish_on_redis(
            event,
            (redis_payload(**self._redis_payload_keys(event, instance)) | instance.redis_payload()),
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def langs(request):
    languages = models.Language.objects.all()
    serializer = serializers.LanguageSerializer(languages, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "healthy"}, status=200)
