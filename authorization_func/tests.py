from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class LoginTest(APITestCase):
    def setUp(self):
        # Создайте пользователя для тестирования входа
        self.user = User.objects.create_user(
            email="test@example.com",
            password="mypassword"
        )

    def test_user_login(self):
        # Данные для входа
        login_data = {
            "email": "test@example.com",
            "password": "mypassword"
        }

        # Отправьте запрос на вход
        response = self.client.post(reverse("login"), login_data, format="json")

        # Проверьте, что вход выполнен успешно (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
