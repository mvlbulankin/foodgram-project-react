from django.core.validators import RegexValidator, validate_slug
from django.db import models


class Tag(models.Model):
    color = models.CharField(
        "Цвет",
        max_length=7,
        unique=True,
        validators=(
            RegexValidator(
                regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                message="Укажите существующий цвет в формате hex",
            ),
        ),
    )
    name = models.CharField(
        "Название тега",
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        "Слаг",
        max_length=200,
        unique=True,
        validators=(validate_slug,)
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
