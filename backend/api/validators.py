from rest_framework.validators import ValidationError

from ingredients.models import Ingredient
from tags.models import Tag


def validate_ingredients(data):
    if not data:
        raise ValidationError({"ingredients": ["Обязательное поле."]})
    unique_ingredient = []
    for ingredient in data:
        if not ingredient.get("id"):
            raise ValidationError(
                {"ingredients": ["Неверный id ингредиента."]}
            )
        id = ingredient.get("id")
        if not Ingredient.objects.filter(id=id).exists():
            raise ValidationError(
                {"ingredients": ["Ингредиента не существует."]}
            )
        if id in unique_ingredient:
            raise ValidationError(
                {"ingredients": ["Нельзя выбрать один ингридиент дважды"]}
            )
        unique_ingredient.append(id)
        amount = int(ingredient.get("amount"))
        if amount < 1:
            raise ValidationError(
                {"amount": ["Количество не может быть менее 1."]}
            )
    return data


def validate_tags(data):
    if not data:
        raise ValidationError({"tags": ["Обязательное поле."]})
    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError({"tags": ["Тега не существует."]})
    return data
