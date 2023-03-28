from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet


app_name = 'api'

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
