import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == "me":
        raise ValidationError(
            "Недопустимое имя пользователя!"
        )
    if not bool(re.match(r"^[\w.@+-]+$", value)):
        incorrect_symbols = re.findall("[^\\w.@+-]", value)
        raise ValidationError(
            f"Введены недопустимые символы: {' '.join(incorrect_symbols)}",
        )
    return value
