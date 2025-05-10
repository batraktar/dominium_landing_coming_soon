import json
from decimal import Decimal

import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from house.models import Property, PropertyType
from accounts.models import Favorite
from datetime import date
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

TELEGRAM_TOKEN = "7639849573:AAFfoDuLlhgDj0wuOw6qzEfFHl6pLTnE8ik"
CHAT_IDS = [396360105, 7679436754]  # Список ID

@login_required
def liked_properties_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    properties = [fav.property for fav in favorites]
    return render(request, 'likes.html', {'properties': properties})

@require_POST
@login_required
def toggle_like(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property)

    if not created:
        favorite.delete()
        return JsonResponse({'status': 'unliked'})
    return JsonResponse({'status': 'liked'})

def get_exchange_rates():
    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
    response = requests.get(url)
    data = response.json()

    usd_rate = next((float(item['sale']) for item in data if item['ccy'] == 'USD'), None)
    eur_rate = next((float(item['sale']) for item in data if item['ccy'] == 'EUR'), None)

    return {
        'USD': usd_rate,
        'EUR': eur_rate
    }

# Приклад використання
rates = get_exchange_rates()
print(f"USD: {rates['USD']} грн, EUR: {rates['EUR']} грн")

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


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug)
    images = property.images.all()
    property.absolute_url = request.build_absolute_uri(property.get_absolute_url())
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
        room_values = q.get("rooms", "")
        if room_values:
            room_list = [r.strip() for r in room_values.split(",") if r.strip()]
            exact_rooms = []
            gte_5 = False

            for r in room_list:
                if r == "5+":
                    gte_5 = True
                elif r.isdigit():
                    exact_rooms.append(int(r))

            room_filter = Q()
            if exact_rooms:
                room_filter |= Q(rooms__in=exact_rooms)
            if gte_5:
                room_filter |= Q(rooms__gte=5)

            queryset = queryset.filter(room_filter)


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

        rates = get_exchange_rates()
        usd_rate = Decimal(rates.get('USD') or 40)
        eur_rate = Decimal(rates.get('EUR') or 43.5)

        for prop in context['properties']:
            prop.price_usd = round(prop.price / usd_rate)
            prop.price_eur = round(prop.price / eur_rate)

        context["room_options"] = ["", "1", "2", "3", "4", "5+"]
        context['found_count'] = context['properties'].count()
        context['sort_option'] = self.request.GET.get("sort", "price_asc")
        context['property_types'] = PropertyType.objects.all()
        context['usd_rate'] = usd_rate
        context['eur_rate'] = eur_rate
        context['today_date'] = date.today().strftime('%d.%m.%Y')



        return context

def signup(request):
    return render(request, 'partials/auth/sign-up.html')
