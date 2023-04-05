from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
        blank=False
    )
    password = models.CharField(
        "Пароль",
        max_length=150,
        blank=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username, ]
    )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписок."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscribe'
            )
        ]
