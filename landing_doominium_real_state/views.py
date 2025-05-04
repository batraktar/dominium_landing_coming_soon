import json
from decimal import Decimal

import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from house.models import Property, PropertyType

TELEGRAM_TOKEN = "7639849573:AAFfoDuLlhgDj0wuOw6qzEfFHl6pLTnE8ik"
CHAT_IDS = [396360105, 7679436754]  # Список ID


def search_properties(request):
    sort_option = request.GET.get("sort", "price_asc")

    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "area_asc": "area",
        "area_desc": "-area",
        "date": "-created_at",
    }

    sort_field = sort_map.get(sort_option, "price")

    # фільтри (приклад — заміни на свої)
    queryset = Property.objects.all()
    if request.GET.get("rooms"):
        queryset = queryset.filter(rooms=request.GET["rooms"])
    if request.GET.get("property_type"):
        queryset = queryset.filter(property_type_id=request.GET["property_type"])
    # додай інші фільтри...

    properties = queryset.order_by(sort_field)

    context = {
        "properties": properties,
        "found_count": properties.count(),
        "sort_option": sort_option,
    }
    return render(request, "property_search_results.html", context)


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

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET

        # 🔍 Пошук по тексту
        query = q.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(address__icontains=query) |
                Q(description__icontains=query)
            )

        # 🔹 Тип нерухомості
        property_type_slugs = q.getlist("property_type")
        if property_type_slugs:
            queryset = queryset.filter(property_type__slug__in=property_type_slugs)

        # 🔹 Площа
        if q.get("area_min"):
            queryset = queryset.filter(area__gte=q["area_min"])
        if q.get("area_max"):
            queryset = queryset.filter(area__lte=q["area_max"])

        # 🔹 Ціна
        if q.get("price_min"):
            queryset = queryset.filter(price__gte=q["price_min"])
        if q.get("price_max"):
            queryset = queryset.filter(price__lte=q["price_max"])

        # 🔹 Кімнати
        if q.get("rooms"):
            if q["rooms"] == "5+":
                queryset = queryset.filter(rooms__gte=5)
            else:
                queryset = queryset.filter(rooms=q["rooms"])

        # 🔹 Сортування
        sort_option = q.get("sort", "price_asc")
        sort_map = {
            "price_asc": "price",
            "price_desc": "-price",
            "area_asc": "area",
            "area_desc": "-area",
            "date": "-created_at",
        }
        return queryset.order_by(sort_map.get(sort_option, "price"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usd_rate = Decimal('40')
        eur_rate = Decimal('43.5')

        for prop in context['properties']:
            prop.price_usd = round(prop.price / usd_rate)
            prop.price_eur = round(prop.price / eur_rate)

        context['found_count'] = context['properties'].count()
        context['sort_option'] = self.request.GET.get("sort", "price_asc")
        context['property_types'] = PropertyType.objects.all()

        return context

def landing(request):
    return render(request, 'landing_dominium.html')
