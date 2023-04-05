from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer
