# Generated by Django 4.1.7 on 2023-04-22 21:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0003_alter_ingredientamount_ingredient_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="favorite",
            options={"verbose_name": "Избранное", "verbose_name_plural": "Избранные"},
        ),
        migrations.AlterModelOptions(
            name="ingredientamount",
            options={
                "verbose_name": "Количество ингредиента",
                "verbose_name_plural": "Количество ингредиентов",
            },
        ),
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ("-pub_date",),
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
            },
        ),
        migrations.AlterModelOptions(
            name="shoppingcart",
            options={
                "verbose_name": "Список покупок",
                "verbose_name_plural": "Список покупок",
            },
        ),
        migrations.AlterField(
            model_name="ingredientamount",
            name="amount",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1, "Количество ингридиента не может быть менее единицы"
                    )
                ]
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1, "Время приготовления не может быть менее одной минуты"
                    )
                ],
                verbose_name="Время приготовления",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(upload_to="recipes/", verbose_name="Изображение"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(max_length=200, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="text",
            field=models.TextField(verbose_name="Описание рецепта"),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopping_cart",
                to="recipes.recipe",
            ),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopping_cart",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
