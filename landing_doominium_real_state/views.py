import json
from decimal import Decimal

import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from house.models import Property

TELEGRAM_TOKEN = "7639849573:AAFfoDuLlhgDj0wuOw6qzEfFHl6pLTnE8ik"
CHAT_IDS = [396360105, 7679436754]  # Список ID


@csrf_exempt
def consultation_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        property_url = request.POST.get("property", "Не вказано").strip()

        errors = []

        if not name:
            errors.append("Імʼя обовʼязкове.")
        if not phone:
            errors.append("Номер телефону обовʼязковий.")
        if not message:
            errors.append("Повідомлення обовʼязкове.")

        if email and "@" not in email:
            errors.append("Некоректна пошта.")

        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        text = f"""
📩 *Нова заявка на консультацію*  
👤 *Ім'я:* {name}  
📞 *Телефон:* {phone}  
✉️ *Пошта:* {email or "Немає"}  
📝 *Повідомлення:* {message}  
🔗 *Посилання на об'єкт:* {property_url}
        """

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        send_errors = []

        for chat_id in CHAT_IDS:
            payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                send_errors.append({"chat_id": chat_id, "error": response.text})

        if send_errors:
            return JsonResponse({"status": "error", "details": send_errors}, status=500)

        return JsonResponse({"status": "ok"}, status=200)

    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    images = property.images.all()
    main_image = images.filter(is_main=True).first() or images.first()
    image_urls = [img.image.url for img in images]
    return render(request, 'property_detail.html', {
        "property": property,
        "main_image": main_image,
        "property_images_json": json.dumps(image_urls),
    })


def base(request):
    properties = Property.objects.order_by('-created_at')[:3]  # топ 3
    return render(request, 'home.html', {'properties': properties})


class SearchFiltersView(ListView):
    model = Property
    context_object_name = 'properties'
    template_name = 'search_filters.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usd_rate = Decimal('40')
        eur_rate = Decimal('43.5')

        for prop in context['properties']:
            prop.price_usd = round(prop.price / usd_rate)
            prop.price_eur = round(prop.price / eur_rate)

        return context


def landing(request):
    return render(request, 'landing_dominium.html')
