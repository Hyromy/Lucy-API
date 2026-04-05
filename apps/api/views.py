from rest_framework import viewsets
from . import models, serializers

class GuildViewSet(viewsets.ModelViewSet):
    queryset = models.Guild.objects.all()
    serializer_class = serializers.GuildSerializer
