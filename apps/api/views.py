from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import models, serializers

class GuildViewSet(viewsets.ModelViewSet):
    queryset = models.Guild.objects.all()
    serializer_class = serializers.GuildSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'healthy'}, status = 200)
