# Generated by Django 4.1.7 on 2023-04-22 21:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ingredients", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredient",
            options={
                "ordering": ("id",),
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
            },
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="measurement_unit",
            field=models.CharField(max_length=200, verbose_name="Единицы измерения"),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(max_length=200, verbose_name="Название ингредиента"),
        ),
    ]
