# apps/core/views.py
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    """
    Главная страница сайта.
    Если пользователь не авторизован — показать приветствие и ссылки на вход/регистрацию.
    Если авторизован — показать приветствие с именем пользователя.
    """
    context = {}
    if request.user.is_authenticated:
        context["username"] = request.user.username
    return render(request, "core/index.html", context)
