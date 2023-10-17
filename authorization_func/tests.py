from django.test import TestCase
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

# Create your tests here.

class OTPCodeTest(APITestCase):
    def test_otp_code_sent_on_registration(self):
        # Создайте данные для регистрации пользователя
        registration_data = {
            "email": "wiyoces635@cindalle.com",
            "name": "Velag",
            "surname": "Velag2",
            "phone_number": "+123456789",
            "password": "kopeika2",
            "repeat_password": "kopeika2",  # Сделайте совпадающим с паролем
        }

        # Сделайте запрос на регистрацию пользователя
        response = self.client.post(reverse("register"), registration_data, format="json")

        # Проверьте, что регистрация прошла успешно (HTTP 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверьте, что внутри электронного письма есть OTP-код
        self.assertEqual(len(mail.outbox), 1)  # Убедитесь, что было отправлено одно письмо
        self.assertIn("Your OTP Code is:", mail.outbox[0].body)  # Проверьте наличие OTP-кода в тексте письма
