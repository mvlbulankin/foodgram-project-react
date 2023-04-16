from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from fpdf import FPDF
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import CustomSearchFilter, RecipeFilter
from .permissions import AuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    SimpleRecipeSerializer,
    SubscriptionSerializer,
    TagSerializer,
)
from ingredients.models import Ingredient
from recipes.models import Favorite, IngredientAmount, Recipe, ShoppingCart
from tags.models import Tag
from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()

    @action(
        detail=False,
        url_path="subscriptions",
        url_name="subscriptions",
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="subscribe",
        url_name="subscribe",
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {"errors": "Нельзя подписаться/отписаться на/от себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription = Subscription.objects.filter(author=author, user=user)
        if request.method == "POST":
            if subscription.exists():
                return Response(
                    {"errors": "Нельзя подписаться повторно"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = Subscription.objects.create(author=author, user=user)
            serializer = SubscriptionSerializer(
                queryset, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            if not subscription.exists():
                return Response(
                    {"errors": "Нельзя отписаться повторно"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [CustomSearchFilter]
    queryset = Ingredient.objects.all()
    pagination_class = None
    search_fields = ("^name",)
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add(self, model, user, pk, name):
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if relation.exists():
            return Response(
                {"errors": f"Нельзя повторно добавить рецепт в {name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.create(user=user, recipe=recipe)
        serializer = SimpleRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_relation(self, model, user, pk, name):
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if not relation.exists():
            return Response(
                {"errors": f"Нельзя повторно удалить рецепт из {name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="favorite",
        url_name="favorite",
    )
    def favorite(self, request, pk=None):
        user = request.user
        if request.method == "POST":
            name = "избранное"
            return self.add(Favorite, user, pk, name)
        if request.method == "DELETE":
            name = "избранного"
            return self.delete_relation(Favorite, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="shopping_cart",
        url_name="shopping_cart",
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        if request.method == "POST":
            name = "список покупок"
            return self.add(ShoppingCart, user, pk, name)
        if request.method == "DELETE":
            name = "списка покупок"
            return self.delete_relation(ShoppingCart, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=["get"],
        detail=False,
        url_path="download_shopping_cart",
        url_name="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            IngredientAmount.objects.filter(recipe__sh_cart__user=user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(Sum("amount", distinct=True))
        )
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()
        pdf.add_font(
            "DejaVu", "", "./recipes/fonts/DejaVuSansCondensed.ttf", uni=True
        )
        pdf.set_font("Dejavu", "", 16)
        pdf.cell(40, 10, "Список покупок:", 0, 1)
        pdf.cell(40, 10, "", 0, 1)
        pdf.set_font("Dejavu", "", 12)
        pdf.cell(100, 10, "Название продукта")
        pdf.cell(100, 10, "Количество")
        pdf.ln()
        pdf.line(10, 30, 150, 30)
        pdf.line(10, 40, 150, 40)
        for num, ingredient in enumerate(ingredients):
            amount = ingredient["amount__sum"]
            name = ingredient["ingredient__name"]
            unit = ingredient["ingredient__measurement_unit"]
            pdf.cell(100, 10, f"{num + 1}. {name}")
            pdf.cell(100, 10, f"{amount} {unit}")
            pdf.ln()
        pdf.output("shopping_cart.pdf", "F")
        return FileResponse(
            open("shopping_cart.pdf", "rb"),
            as_attachment=True,
            content_type="application/pdf",
        )
