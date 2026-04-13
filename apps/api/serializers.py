from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models


class GuildSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=[UniqueValidator(queryset=models.Guild.objects.all())])

    class Meta:
        model = models.Guild
        fields = [
            "id",
            "name",
            "lang",
            "joined_at",
            "updated_at",
            "version",
        ]
        read_only_fields = [
            "joined_at",
            "updated_at",
            "version",
        ]

    def validate_id(self, value):
        if self.instance and self.instance.id != value:
            raise serializers.ValidationError("ID cannot be changed.")

        return value
