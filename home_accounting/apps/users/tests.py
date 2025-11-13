# apps/users/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 200)
