from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField

from .validators import validate_ingredients
from ingredients.models import Ingredient
from recipes.models import Favorite, IngredientAmount, Recipe, ShoppingCart
from tags.models import Tag
from users.models import Subscription, User


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed",
        )
        # write_only_fields = ("password",)

    def get_is_subscribed(self, obj):
        user_id = self.context.get("request").user.id
        return Subscription.objects.filter(
            author=obj.id, user=user_id
        ).exists()

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class SubscriptionSerializer(CustomUserSerializer):
    email = serializers.EmailField(
        source="author.email",
        read_only=True,
    )
    first_name = serializers.CharField(
        source="author.first_name",
        read_only=True,
    )
    id = serializers.IntegerField(
        source="author.id",
        read_only=True,
    )
    # is_subscribed = serializers.SerializerMethodField()
    last_name = serializers.CharField(
        source="author.last_name",
        read_only=True,
    )
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source="author.recipes.count",
        read_only=True,
    )
    username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    class Meta:
        model = Subscription
        fields = (
            "email",
            "id",
            "is_subscribed",
            "first_name",
            "last_name",
            "recipes",
            "recipes_count",
            "username",
        )
        # read_only_fields = (
        #     "email",
        #     "id",
        #     "first_name",
        #     "last_name",
        #     "recipes_count",
        #     "username",
        # )

    # def get_is_subscribed(self, obj):
    #     user = self.context.get("request").user
    #     return Subscription.objects.filter(
    #         author=obj.author, user=user
    #     ).exists()

    def get_recipes(self, obj):
        limit = self.context.get("request").GET.get("recipes_limit")
        recipe_obj = obj.author.recipes.all()
        if limit:
            recipe_obj = recipe_obj[:int(limit)]
        serializer = SimpleRecipeSerializer(recipe_obj, many=True)
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "color",
            "id",
            "name",
            "slug",
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "measurement_unit",
            "name",
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source="ingredient.id",
        read_only=True,
    )
    name = serializers.CharField(
        source="ingredient.name",
        read_only=True,
    )
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit",
        read_only=True,
    )

    class Meta:
        model = IngredientAmount
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientAmountSerializer(
        read_only=True,
        many=True,
        source="ingredientamount_set",
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "author",
            "cooking_time",
            "id",
            "image",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "tags",
            "text",
        )

    def get_is_favorited(self, obj):
        user_id = self.context.get("request").user.id
        return Favorite.objects.filter(user=user_id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user_id = self.context.get("request").user.id
        return ShoppingCart.objects.filter(
            user=user_id, recipe=obj.id
        ).exists()

    def create_ingredient_amount(self, valid_ingredients, recipe):
        for ingredient_data in valid_ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_data.get("id")
            )
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data.get("amount"),
            )

    def create_tags(self, validated_data, recipe):
        valid_tags = validated_data.get("tags")
        tags = Tag.objects.filter(id__in=valid_tags)
        recipe.tags.set(tags)

    def create(self, validated_data):
        valid_ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags(self.initial_data, recipe)
        self.create_ingredient_amount(valid_ingredients, recipe)
        return recipe

    def validate(self, data):
        ingredients = self.initial_data.get("ingredients")
        valid_ingredients = validate_ingredients(ingredients)
        data["ingredients"] = valid_ingredients
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.save()
        instance.tags.remove()
        self.create_tags(self.initial_data, instance)
        instance.ingredientamount_set.filter(recipe__in=[instance.id]).delete()
        valid_ingredients = validated_data.get(
            "ingredients", instance.ingredients
        )
        self.create_ingredient_amount(valid_ingredients, instance)
        return instance


class SimpleRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "cooking_time",
            "id",
            "image",
            "name",
        )
        read_only_fields = (
            "cooking_time",
            "id",
            "image",
            "name",
        )
