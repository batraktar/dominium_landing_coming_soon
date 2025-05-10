import sys
import requests
from os.path import basename
from urllib.parse import urlparse
from urllib.request import urlopen
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Property, PropertyType, DealType, PropertyImage
from .utils.html_parser import parse_property_from_html

sys.stdout.reconfigure(encoding='utf-8')


def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and parsed.netloc
    except:
        return False


def generate_unique_slug_for_property_type(name):
    from django.utils.text import slugify
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    while PropertyType.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


@csrf_exempt
def import_property_by_url(request):
    try:
        if request.method != "POST":
            return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

        url = request.POST.get("url")
        if not url or not is_valid_url(url):
            return JsonResponse({"status": "error", "message": "Некоректна URL-адреса"}, status=400)

        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"status": "error", "message": "Не вдалося завантажити HTML"}, status=400)

        temp_path = "/tmp/property.html"
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        data = parse_property_from_html(temp_path)

        # ✅ Забезпечуємо унікальність slug
        property_type_obj, created = PropertyType.objects.get_or_create(name=data["property_type"])

        # 🛠 Додаємо slug тільки якщо об'єкт щойно створений або slug порожній
        if created or not property_type_obj.slug:
            property_type_obj.slug = generate_unique_slug_for_property_type(property_type_obj.name)
            property_type_obj.save()


        deal_type_obj, _ = DealType.objects.get_or_create(name=data["deal_type"])

        prop = Property(
            title=data["title"],
            address=data["address"],
            price=data["price"],
            area=int(data["area"]),
            rooms=int(data["rooms"]),
            description=data["description"],
            property_type=property_type_obj,
            deal_type=deal_type_obj,
        )
        prop.save()
        prop.save()  # вдруге для генерації slug

        for i, img_url in enumerate(data["gallery"]):
            try:
                response = urlopen(img_url)
                file_name = basename(img_url.split("?")[0]) or f'image-{i}.jpg'
                image_file = ContentFile(response.read())
                image_instance = PropertyImage(property=prop, is_main=(i == 0))
                image_instance.image.save(file_name, image_file, save=True)
            except Exception as e:
                print("⚠️ Error loading image:", e)

        return JsonResponse({"status": "ok", "id": prop.id})

    except Exception as e:
        print("❌ Error:", str(e))
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
