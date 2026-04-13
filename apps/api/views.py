from json import dumps as json_dumps
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from redis import from_url as redis_from_url

from . import models, serializers
from project.config import config

redis_client = redis_from_url(config.REDIS_URL)


def _publish_on_redis(channel: str, payload: dict):
    """Publish a message on Redis. The payload is serialized to JSON before publishing."""

    try:
        redis_client.publish(channel, json_dumps(payload))
    except Exception as e:
        print(f"Failed to publish on Redis: {e}")


def _redis_payload(*, event: str, version: int, updated_at: str, source: str) -> dict:
    """Helper function to create a standardized payload for Redis messages. This ensures that all messages have a consistent structure."""

    return {
        "event": event,
        "version": version,
        "updated_at": updated_at,
        "source": source,
    }


class GuildViewSet(viewsets.ModelViewSet):
    queryset = models.Guild.objects.all()
    serializer_class = serializers.GuildSerializer

    _event_name = "guild.settings.update"

    def _guild_payload(self, instance: models.Guild) -> dict:
        """Helper function to create a standardized payload for Redis messages related to guild settings."""

        return {
            "id": instance.id,
            "lang": instance.lang,
        }

    def perform_update(self, serializer: serializers.GuildSerializer):
        instance: models.Guild = serializer.save()
        instance.version += 1
        instance.save(update_fields=["version"])

        _publish_on_redis(
            self._event_name,
            (
                _redis_payload(
                    event=self._event_name,
                    version=instance.version,
                    updated_at=instance.updated_at.isoformat(),
                    source=self.request.headers.get("X-Source", "unknown"),
                )
                | self._guild_payload(instance)
            ),
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "healthy"}, status=200)
