# Generated by Django 4.1.7 on 2023-04-05 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredientamount_ingredient_and_more'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
