from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    color = models.CharField(
        "Цвет",
        max_length=7,
        unique=True,
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
        validators=[
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$",
                message="Только латинские буквы, дефис и нижнее подчеркивание",
            )
        ]
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
