# apps/users/urls_template.py
from django.urls import path
from .views_template import RegisterTemplateView, LoginTemplateView, ProfileTemplateView, LogoutTemplateView

app_name = "users_template"

urlpatterns = [
    path("register/", RegisterTemplateView.as_view(), name="register"),
    path("login/", LoginTemplateView.as_view(), name="login"),
    path("logout/", LogoutTemplateView.as_view(), name="logout"),
    path("profile/", ProfileTemplateView.as_view(), name="profile"),
]
