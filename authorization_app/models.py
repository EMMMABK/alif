from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import pyotp

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    otp_secret = models.CharField(max_length=16, null=True, blank=True)
    last_otp_sent = models.DateTimeField(null=True, blank=True)

    def can_resend_otp(self):
        if not self.last_otp_sent:
            return True
        time_difference = timezone.now() - self.last_otp_sent
        return time_difference.total_seconds() > 60  # Ограничение на отправку каждую минуту

    def generate_otp(self):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()
        totp = pyotp.TOTP(self.otp_secret)
        return totp.now()
