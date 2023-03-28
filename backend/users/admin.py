from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


class CustomUserAdmin(UserAdmin):
    """Админка для модели User."""
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    ordering = ('pk',)


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
