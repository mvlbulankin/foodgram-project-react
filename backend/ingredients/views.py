from rest_framework import viewsets

from .filters import CustomSearchFilter
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [CustomSearchFilter]
    queryset = Ingredient.objects.all()
    pagination_class = None
    search_fields = ("^name",)
    serializer_class = IngredientSerializer
