import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == "me":
        raise ValidationError(
            "Недопустимое имя пользователя!"
        )
    if not bool(re.match(r"^[\w.@+-]+$", value)):
        raise ValidationError(
            "Только латинские буквы, цифры, дефис и нижнее подчеркивание",
        )
    return value
