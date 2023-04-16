from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    cooking_time = models.IntegerField(
        "Время приготовления",
        validators=[MinValueValidator(1, "Не может быть менее единицы")],
    )
    image = models.ImageField(
        "Изображение",
        upload_to="recipes/",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount",
    )
    name = models.CharField(
        "Название",
        max_length=200,
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        db_index=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
    )
    text = models.TextField(
        "Описание рецепта",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_favorite_recipe",
            )
        ]


class IngredientAmount(models.Model):
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Не может быть менее единицы")]
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиентов"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="sh_cart",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sh_cart",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_cart_recipe",
            )
        ]
