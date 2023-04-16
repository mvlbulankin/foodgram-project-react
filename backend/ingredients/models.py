from django.db import models


class Ingredient(models.Model):
    measurement_unit = models.CharField(
        "Единицы измерения",
        max_length=200,
    )
    name = models.CharField(
        "Название ингредиента",
        max_length=200,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name
