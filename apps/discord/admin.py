from django.contrib import admin

from .models import (
    Member,
)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    readonly_fields = ["id", "user", "access_token", "refresh_token"]

    def get_fields(self, request, obj=None):
        return ["id", "user"]
