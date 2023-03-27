from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
# from reviews.models import Category, Genre, Review, Title
from users.models import User

# from .filters import TitleFilter
# from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdminAuthorModeratorOrReadOnly, IsAdminOnly,
                          IsAdminOrReadOnly)
from .serializers import (SignUpSerializer, TokenSerializer, UserMeSerializer,
                          UserSerializer)


class SignUpView(generics.CreateAPIView):
    """Регистрация нового пользователя по username и email.
    На электронную почту пользователю отправляется
    код подтверждения. Если пользователь уже зарегистрирован,
    он получает обновлённый код подтверждения.
    """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Получение кода подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}.',
            from_email=settings.EMAIL_ADMIN,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(generics.CreateAPIView):
    """Получение токена по имени пользователя и коду подтверждения."""
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status.HTTP_200_OK)
        return Response(
            {'message': 'Неверный код подтверждения.'},
            status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователем. Доступно для администраторов."""
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def edit_profile(self, request):
        """Редактирование собственной страницы.
        Доступно для аутентифицированных пользователей.
        Роль пользователя изменить нельзя.
        """
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(self.request.user)
        return Response(serializer.data)
