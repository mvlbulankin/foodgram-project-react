from django.contrib import admin

from .models import Tag


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
    search_fields = (
        "name",
    )
