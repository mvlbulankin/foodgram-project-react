from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, TokenObtainView, UserViewSet

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/signup/", SignUpView.as_view()),
    path("auth/token/", TokenObtainView.as_view()),
    path("", include(router.urls)),
]
