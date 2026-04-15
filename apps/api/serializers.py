from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = ["code", "name"]
        read_only_fields = ["code", "name"]


class GuildSerializer(serializers.ModelSerializer):
    id = serializers.CharField(validators=[UniqueValidator(queryset=models.Guild.objects.all())])
    lang = serializers.SlugRelatedField(
        slug_field="code",
        queryset=models.Language.objects.all(),
    )

    class Meta:
        model = models.Guild
        fields = [
            "id",
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

    def to_representation(self, instance):
        self.fields["lang"] = LanguageSerializer()
        return super().to_representation(instance)
