from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    gender = forms.ChoiceField(
        choices=CustomUser.GENDER_CHOICES,
        required=False,
        label="Пол",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    avatar = forms.ImageField(
        required=False,
        label="Аватар",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    is_parent = forms.BooleanField(
        required=False,
        label="Я родитель",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "gender",
            "avatar",
            "is_parent"
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    # 🔥 Проверяем уникальность email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")
