from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'

    role = models.CharField(
        'Роль',
        max_length=50,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username, ]
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
        blank=True
    )
    password = models.CharField(
        "Пароль",
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.username
