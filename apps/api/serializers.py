from rest_framework import serializers
from . import models

class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guild
        fields = [
            "id",
            "name",
            "lang",
            "joined_at",
        ]
        read_only_fields = [
            "joined_at",
        ]
