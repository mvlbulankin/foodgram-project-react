# from django_filters import ModelMultipleChoiceFilter
# from django_filters.rest_framework import FilterSet, filters
# from rest_framework.filters import SearchFilter
#
# from recipes.models import Recipe
# from tags.models import Tag
#
#
# class CustomSearchFilter(SearchFilter):
#     search_param = "name"
#
#
# class RecipeFilter(FilterSet):
#     author = filters.CharFilter(lookup_expr='exact')
#     is_favorited = filters.BooleanFilter(
#         field_name='is_favorited',
#         method='filter',
#     )
#     is_in_shopping_cart = filters.BooleanFilter(
#         field_name='is_in_shopping_cart',
#         method='filter',
#     )
#     tags = ModelMultipleChoiceFilter(
#         queryset=Tag.objects.all(),
#         field_name='tags__slug',
#         to_field_name='slug',
#     )
#
#     class Meta:
#         model = Recipe
#         fields = (
#             'author',
#             'tags',
#         )
#
#     def filter(self, queryset, name, value):
#         if name == 'is_favorited' and value:
#             queryset = queryset.filter(
#                 favorite__user=self.request.user
#             )
#         if name == 'is_in_shopping_cart' and value:
#             queryset = queryset.filter(
#                 shopping_cart__user=self.request.user
#             )
#         return queryset


from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe
from tags.models import Tag


class CustomSearchFilter(SearchFilter):
    search_param = "name"


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(
        method="filter_favorited"
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_shopping_cart"
    )
    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

    def filter_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
        )
