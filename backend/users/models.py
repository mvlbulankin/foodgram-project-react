from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username


class User(AbstractUser):
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
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username, ]
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.CharField(
        "Пароль",
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель для подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscribe'
            )
        ]
