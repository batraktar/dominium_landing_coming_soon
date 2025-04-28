import os
from urllib.parse import urlsplit
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from house.models import Property, PropertyType, DealType, PropertyImage


def get_deal_type(title):
    title_lower = title.lower()
    rent_keywords = [
        "оренда", "орендую", "орендувати", "орендується",
        "здається", "здаю", "здають", "здам", "здача", "зняти", "зніму"
    ]
    sale_keywords = [
        "продаж", "продам", "продається", "продаю", "продають", "купити", "куплю"
    ]
    for word in rent_keywords:
        if word in title_lower:
            return "Оренда"
    for word in sale_keywords:
        if word in title_lower:
            return "Продаж"
    return "Інше"


def get_property_type(title):
    title_lower = title.lower()
    if "будинок" in title_lower or "котедж" in title_lower or "дуплекс" in title_lower:
        return "Будинок"
    elif "квартир" in title_lower or "апартаменти" in title_lower:
        return "Квартира"
    elif "земельн" in title_lower or "ділянка" in title_lower or "соток" in title_lower:
        return "Земельна ділянка"
    elif "комерц" in title_lower or "офіс" in title_lower or "магазин" in title_lower:
        return "Комерційна нерухомість"
    return "Інше"


def parse_property_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    title = soup.find("h2").text.strip()
    address = soup.find("h3").text.strip()

    price_text = soup.select_one(".pdf-header-contacts strong")
    price = int(price_text.text.strip().replace(" ", "").replace("$", "")) if price_text else 0

    detail = soup.select_one(".pdf-detail")
    rooms, area = 0, 0
    if detail:
        spans = detail.find_all("span")
        for span in spans:
            if "кімнат" in span.text.lower():
                try:
                    rooms = int(span.text.strip().split()[0])
                except:
                    pass

    area_icon = soup.select_one('img[src*="_area-icon.png"]')
    if area_icon:
        parent = area_icon.find_parent("span")
        if parent and parent.text:
            try:
                area = float(parent.text.strip().split("/")[0])
            except:
                pass

    # Парсимо опис з HTML збереженням абзаців
    pdf_blocks = soup.find_all("div", class_="pdf-block")
    description_html = str(pdf_blocks[1]) if len(pdf_blocks) > 1 else ""

    main_image_tag = soup.select_one(".pdf-img img")
    main_image = main_image_tag["src"] if main_image_tag else ""
    gallery = [a["href"] for a in soup.select("#estate-images a") if a.has_attr("href")]

    property_type = get_property_type(title)
    deal_type = get_deal_type(title)

    return {
        "title": title,
        "address": address,
        "price": price,
        "area": area,
        "rooms": rooms,
        "description": description_html,
        "main_image": main_image,
        "gallery": gallery,
        "property_type": property_type,
        "deal_type": deal_type,
    }


def import_property_from_html(html_path):
    data = parse_property_from_html(html_path)

    property_type_obj, _ = PropertyType.objects.get_or_create(name=data["property_type"])
    deal_type_obj, _ = DealType.objects.get_or_create(name=data["deal_type"])

    prop = Property.objects.create(
        title=data["title"],
        address=data["address"],
        price=data["price"],
        area=int(data["area"]),
        rooms=int(data["rooms"]),
        description=data["description"],
        property_type=property_type_obj,
        deal_type=deal_type_obj,
    )

    # Додаємо головне зображення
    if data["main_image"]:
        image_name = os.path.basename(urlsplit(data["main_image"]).path)
        try:
            image_content = ContentFile(urlopen(data["main_image"], timeout=10).read(), name=image_name)
            PropertyImage.objects.create(property=prop, image=image_content, is_main=True)
        except Exception as e:
            print("⚠️ Error loading main image:", e)

    # Додаємо інші зображення
    for img_url in data["gallery"]:
        image_name = os.path.basename(urlsplit(img_url).path)
        try:
            response = urlopen(img_url, timeout=10)
            content_type = response.info().get_content_type()
            if not content_type.startswith("image"):
                continue
            image_content = ContentFile(response.read(), name=image_name)
            PropertyImage.objects.create(property=prop, image=image_content, is_main=False)
        except Exception as e:
            print("⚠️ Skipping invalid image:", img_url, str(e))
            continue

    return prop
