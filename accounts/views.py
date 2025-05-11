from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser, TelegramVerification
from uuid import uuid4
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

User = get_user_model()

@require_GET
def check_telegram_username(request):
    username = request.GET.get('username', '').lstrip('@')
    exists = User.objects.filter(telegram_username=username).exists()
    return JsonResponse({'available': not exists})

def register_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            return render(request, 'partials/auth/email.html', {
                'error': 'Паролі не збігаються'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'partials/auth/email.html', {
                'error': 'Цей email вже використовується'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'partials/auth/email.html', {
                'error': 'Цей username вже зайнятий'
            })

        user = CustomUser.objects.create(
            email=email,
            username=username,
            telegram_username=username,  # 👈 тут автоматично копіюється
            password=make_password(password),
            is_active=False
        )

        # Надсилання листа
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        domain = get_current_site(request).domain
        link = f"http://{domain}/activate/{uid}/{token}/"

        message = render_to_string('partials/auth/verify_email.html', {
            'user': user,
            'link': link
        })

        # Надсилання листа
        result = send_mail(
            subject='Підтвердження пошти',
            message=message,
            from_email='Dominium <dominium.realty.agency@gmail.com>',
            recipient_list=[email]
        )


        print(f'Email send result: {result}')

        return render(request, 'partials/auth/after-register-email.html', {
            'email': email
        })

    return render(request, 'partials/auth/email.html')



def register_via_telegram(request):
    if request.method == 'POST':
        telegram_username = request.POST.get('telegram_username', '').lstrip('@')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            return render(request, 'partials/auth/telegram.html', {
                'error': 'Паролі не збігаються',
                'telegram_username': telegram_username,
            })

        unique_username = telegram_username or f"user_{uuid4().hex[:8]}"

        user, created = User.objects.get_or_create(
            username=unique_username,
            defaults={
                'telegram_username': telegram_username,
                'password': make_password(password),
                'is_active': True,
            }
        )

        if not created:
            return render(request, 'partials/auth/telegram.html', {
                'error': 'Користувач з таким username вже існує',
            })

        TelegramVerification.objects.create(user=user)

        return render(request, 'partials/auth/after-register-telegram.html', {
            'bot_link': 'https://t.me/dominium_realty_agency_bot'
        })




def verify_telegram_code(request, code):
    verification = get_object_or_404(TelegramVerification, code=code, is_used=False)
    verification.is_used = True
    verification.save()

    user = verification.user
    user.is_telegram_verified = True
    user.save()

    login(request, user)  # автоматичний вхід
    return redirect('/')  # редірект на головну


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password')

        user = CustomUser.objects.filter(
            Q(email__iexact=identifier) | Q(telegram_username__iexact=identifier)
        ).first()

        if user and check_password(password, user.password):
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'partials/auth/login.html', {
                'error': 'Невірний email / username або пароль',
                'email': identifier,
            })

    # GET-запит — просто рендеримо форму без передачі змінних
    return render(request, 'partials/auth/login.html')

from django.contrib.auth import login

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        
        login(request, user)  # <== автоматичний вхід
        return redirect('/')  # <== редірект на головну
    else:
        return render(request, 'partials/auth/email_invalid.html')



def logout_view(request):
    logout(request)
    return redirect('/')