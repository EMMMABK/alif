from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core import mail

class EmailConfirmationTest(APITestCase):
    def test_email_confirmation(self):
        data = {
            "email": "nidiped685@weirby.com"  # Замените на реальный адрес электронной почты
        }

        url = reverse("email-confirmation")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)  # Убедитесь, что было отправлено одно письмо
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.to, ["nidiped685@weirby.com"])  # Убедитесь, что письмо отправлено на правильный адрес
