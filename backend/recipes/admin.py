from django.contrib import admin

from .models import Favorite, IngredientAmount, Recipe, ShoppingCart


@admin.register(Favorite, ShoppingCart)
class FavoriteShoppingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipe",
        "user",
    )
    search_fields = (
        "user__username",
        "recipe__name",
    )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "amount",
        "ingredient",
        "recipe",
    )
    search_fields = (
        "ingredient__name",
        "recipe__name",
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"
    exclude = ("ingredients",)
    list_display = (
        "pk",
        "author",
        "count_added",
        "image",
        "name",
    )
    list_filter = (
        "author",
        "name",
        "tags",
    )
    search_fields = (
        "author__username",
        "name",
        "tags__name",
    )

    def count_added(self, obj):
        return obj.favorite.count()
