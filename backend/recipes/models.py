from django.core.validators import MinValueValidator
from django.db import models

from .validators import validate_time
from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    cooking_time = models.IntegerField(validators=[validate_time])
    image = models.ImageField(upload_to="recipes/")
    ingredients = models.ManyToManyField(
        Ingredient, through="IngredientAmount"
    )
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )
    tags = models.ManyToManyField(Tag, related_name="recipes")
    text = models.TextField()

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Не может быть менее 1")]
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"], name="unique_favorite_recipe"
            )
        ]


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="sh_cart"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sh_cart",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"], name="unique_cart_recipe"
            )
        ]
