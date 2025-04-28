from os.path import basename
from urllib.request import urlopen

import requests
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Property, PropertyType, DealType, PropertyImage
from .utils.html_parser import parse_property_from_html


@csrf_exempt
def import_property_by_url(request):
    try:
        if request.method == "POST":
            url = request.POST.get("url")
            if not url:
                return JsonResponse({"status": "error", "message": "URL не передано"}, status=400)

            response = requests.get(url)
            if response.status_code != 200:
                return JsonResponse({"status": "error", "message": "Не вдалося завантажити HTML"}, status=400)

            temp_path = "/tmp/property.html"
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            data = parse_property_from_html(temp_path)

            property_type_obj, _ = PropertyType.objects.get_or_create(name=data["property_type"])
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

            for i, img_url in enumerate(data["gallery"]):
                try:
                    response = urlopen(img_url)
                    file_name = basename(img_url.split("?")[0])  # назва файлу без query string
                    image_file = ContentFile(response.read())

                    image_instance = PropertyImage(property=prop, is_main=(i == 0))
                    image_instance.image.save(file_name, image_file, save=True)
                except Exception as e:
                    print("⚠️ Error loading image:", e)

            return JsonResponse({"status": "ok", "id": prop.id})

        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

    except Exception as e:
        print("❌ Error:", str(e))  # лог в терміналі
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
