from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'telegram_username', 'email', 'is_telegram_verified', 'is_email_verified', 'is_staff')
    search_fields = ('telegram_username', 'email')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('telegram_username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Verification', {'fields': ('is_telegram_verified', 'is_email_verified')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telegram_username', 'email', 'password1', 'password2')}
        ),
    )
