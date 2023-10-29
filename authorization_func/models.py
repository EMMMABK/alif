from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    password_reset_token = models.CharField(max_length=6, null=True, blank=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_confirmation_code = models.CharField(max_length=6, null=True, blank=True)
    password = models.CharField(max_length=128)
    repeat_password = models.CharField(max_length=128, default='')

    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    university = models.CharField(max_length=255, blank=True)
    faculty = models.CharField(max_length=255, blank=True)
    specialty = models.CharField(max_length=255, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    social_links = models.TextField(blank=True)

    workplace = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    
    short_info = models.TextField(blank=True)
    achievements = models.TextField(blank=True)

    email_confirmed = models.BooleanField(default=False)  

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=6)  
    created_at = models.DateTimeField(auto_now_add=True)
