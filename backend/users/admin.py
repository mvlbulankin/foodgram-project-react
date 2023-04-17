from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Subscription, User


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
