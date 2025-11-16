# apps/users/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_and_profile(self):
        response = self.client.post(reverse("users:register"), {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123456",
            "first_name": "Test",
            "last_name": "User"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("user", data.get("data", {}))
        # получить токен и запросить профиль
        token = data["data"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        profile_resp = self.client.get(reverse("users:profile"))
        self.assertEqual(profile_resp.status_code, 200)
