from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter
from recipes.models import Recipe
from tags.models import Tag


class CustomSearchFilter(SearchFilter):
    search_param = "name"


class RecipeFilter(FilterSet):
    author = filters.CharFilter(lookup_expr='exact')
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='filter',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter',
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def filter(self, queryset, name, value):
        if name == 'is_favorited' and value:
            queryset = queryset.filter(
                favorite__user=self.request.user
            )
        if name == 'is_in_shopping_cart' and value:
            queryset = queryset.filter(
                shopping_cart__user=self.request.user
            )
        return queryset
