from django.db import models


class Ingredient(models.Model):
    measurement_unit = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name
