# apps/users/urls.py
from django.urls import path
from .views import RegisterView, ProfileView
from django.contrib.auth.views import LoginView, LogoutView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register_page"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login_page"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]

