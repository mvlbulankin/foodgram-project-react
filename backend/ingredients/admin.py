from django.contrib import admin

from .models import Ingredient


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
    search_fields = (
        "name",
    )
