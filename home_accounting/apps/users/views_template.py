# apps/users/views_template.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterTemplateView(View):
    template_name = "users/register.html"

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})

class LoginTemplateView(View):
    template_name = "users/login.html"

    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class LogoutTemplateView(View):
    def get(self, request):
        logout(request)
        return render(request, "users/logout.html")


class ProfileTemplateView(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get(self, request):
        return render(request, self.template_name)
