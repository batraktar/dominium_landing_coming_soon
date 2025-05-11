from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, telegram_username=None, email=None, password=None, **extra_fields):
        if not telegram_username and not email:
            raise ValueError("User must have either a telegram_username or an email")
        
        user = self.model(telegram_username=telegram_username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, telegram_username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(telegram_username, password=password, **extra_fields)

