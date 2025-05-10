import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
from house.models import Property


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)  # ← нове поле
    email = models.EmailField(unique=True, blank=True, null=True)
    telegram_username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    is_email_verified = models.BooleanField(default=False)
    is_telegram_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  # ← логін по username
    REQUIRED_FIELDS = ['email']  # ← щоб створити суперкористувача

    objects = CustomUserManager()

    def __str__(self):
        return self.username or self.telegram_username or self.email or "UnknownUser"


    def __str__(self):
        return self.telegram_username or self.email or "UnknownUser"

class TelegramVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {'used' if self.is_used else 'active'}"
    

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='liked_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
        