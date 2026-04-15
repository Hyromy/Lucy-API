from django.contrib import admin

from . import serializers
from .gossiper import redis_payload, publish_on_redis, event_name
from .models import (
    Guild,
    Language,
)


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    fields = ["id", "lang", "joined_at", "updated_at", "version"]

    base_readonly_fields = ["joined_at", "updated_at", "version"]

    list_display = ["id", "lang", "joined_at", "updated_at", "version"]

    def redis_payload_keys(self, event: str, instance: Guild, request) -> dict:
        return {
            "event": event,
            "version": instance.version,
            "updated_at": instance.updated_at.isoformat(),
            "source": "admin panel",
        }

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.base_readonly_fields + ["id"]

        return self.base_readonly_fields

    def save_model(self, request, obj: Guild, form, change):
        if change:
            obj.version += 1

        super().save_model(request, obj, form, change)

        if change:
            event = event_name("guild", "updated")
            publish_on_redis(
                event,
                (
                    redis_payload(**self.redis_payload_keys(event, obj, request))
                    | serializers.GuildSerializer(obj).data
                ),
            )


admin.site.register(Language)
