# apps/users/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ProfileSerializer
from apps.core.mixins import ResponseMixin

User = get_user_model()


class RegisterView(ResponseMixin, generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return self.success_response(
            data={
                "user": ProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            message="Пользователь успешно зарегистрирован."
        )


class ProfileView(ResponseMixin, generics.RetrieveUpdateAPIView):
    """
    Просмотр/редактирование профиля текущего пользователя.
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()
