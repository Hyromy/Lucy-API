import logging
from django.http import StreamingHttpResponse
from json import dumps as json_dumps
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import models, serializers
from .gossiper import (
    publish_on_redis,
    redis_payload,
    event_name,
    redis_client,
)

logger = logging.getLogger(__name__)


def _event_stream():
    pubsub = redis_client.pubsub()
    pubsub.psubscribe("lucy.*")

    try:
        yield f"data: {json_dumps({'status': 'connected'})}\n\n"

        for message in pubsub.listen():
            if message["type"] == "pmessage":
                data = message["data"]
                yield f"data: {data.decode('utf-8') if isinstance(data, bytes) else data}\n\n"

    except Exception as e:
        logger.error("Error occurred while streaming events", exc_info=e)

    finally:
        pubsub.close()


def events(request):
    """Endpoint for streaming guild update events. Clients can connect to this endpoint to receive real-time updates."""

    response = StreamingHttpResponse(_event_stream(), content_type="text/event-stream")

    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    response["Access-Control-Allow-Origin"] = "*"

    return response


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

    def perform_create(self, serializer: serializers.GuildSerializer):
        instance: models.Guild = serializer.save()
        event = event_name("guild", "created")
        publish_on_redis(
            event,
            (
                redis_payload(**self._redis_payload_keys(event, instance))
                | serializers.GuildSerializer(instance).data
            ),
        )

    def perform_update(self, serializer: serializers.GuildSerializer):
        instance: models.Guild = serializer.save()
        instance.version += 1
        instance.save(update_fields=["version"])

        event = event_name("guild", "updated")
        publish_on_redis(
            event,
            (
                redis_payload(**self._redis_payload_keys(event, instance))
                | serializers.GuildSerializer(instance).data
            ),
        )

    def perform_destroy(self, instance: models.Guild):
        event = event_name("guild", "deleted")
        publish_on_redis(
            event,
            (
                redis_payload(**self._redis_payload_keys(event, instance))
                | serializers.GuildSerializer(instance).data
            ),
        )

        super().perform_destroy(instance)


@api_view(["GET"])
def langs(request):
    languages = models.Language.objects.all()
    serializer = serializers.LanguageSerializer(languages, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "healthy"}, status=200)
