from django.contrib import admin

from .models import (
    Guild,
)


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    fields = ["id", "name", "lang", "joined_at", "updated_at", "version"]

    base_readonly_fields = ["joined_at", "updated_at", "version"]

    list_display = ["id", "name", "lang", "joined_at", "updated_at", "version"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.base_readonly_fields + ["id"]

        return self.base_readonly_fields
