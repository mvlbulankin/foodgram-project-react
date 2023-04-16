from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Subscription, User
from ingredients.models import Ingredient
from recipes.models import Favorite, IngredientAmount, Recipe, ShoppingCart
from tags.models import Tag


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = (
        "email",
        "username",
    )
    ordering = ("pk",)
    search_fields = (
        "email",
        "username",
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )
    list_editable = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"
    list_display = (
        "pk",
        "name",
        "color",
        "slug",
    )
    list_editable = (
        "color",
        "name",
        "slug",
    )
    search_fields = ("name",)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"
    exclude = ("ingredients",)
    inlines = (IngredientAmountInline,)
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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "user",
    )
    search_fields = (
        "author__username",
        "user__username",
    )


admin.site.unregister(Group)
