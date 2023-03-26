from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        )


class UserAdmin(ImportExportModelAdmin):
    resource_classes = (UserResource,)
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'password',
    )


admin.site.register(User, UserAdmin)
