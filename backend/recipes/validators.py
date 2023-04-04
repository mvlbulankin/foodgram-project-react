from rest_framework.validators import ValidationError as RFError

from tags.models import Ingredient, Tag


def validate_time(value):
    """Валидация поля модели - время приготовления."""
    if value < 1:
        raise RFError(
            ['Время не может быть менее минуты.']
        )
