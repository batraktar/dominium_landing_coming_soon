import os
from urllib.parse import urlsplit
from urllib.request import urlopen
from uuid import uuid4
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from house.models import Property, PropertyType, DealType, PropertyImage
import logging
from decimal import Decimal, InvalidOperation
logger = logging.getLogger(__name__)


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
    price_raw = price_text.text.strip() if price_text else "0"

    currency = "USD"  # за замовчуванням

    # Пробуємо дістати число з тексту
    price_clean = price_raw.lower().replace(" ", "")

    if "грн" in price_clean:
        currency = "UAH"
        price_clean = price_clean.replace("грн", "")
    elif "$" in price_clean:
        price_clean = price_clean.replace("$", "")

    try:
        price = Decimal(price_clean)
    except InvalidOperation:
        logger.error(f"❌ Неможливо розпарсити ціну: '{price_raw}'")
        price = Decimal(0)

    rooms = None

# 1. Пошук через іконку з кімнатами (як раніше)
    room_icon = soup.select_one('img[src*="_room-icon.png"]')
    if room_icon:
        parent = room_icon.find_parent("span")
        if parent and parent.text.strip():
            try:
                rooms = int(parent.text.strip().split()[0])
            except Exception as e:
                print("⚠️ Rooms (icon) parse failed:", e)

    # 2. Якщо не знайшли, шукаємо в табличці з <th>Кіл. кімнат</th>
    if rooms is None:
        th = soup.find("th", string=lambda s: s and "Кіл. кімнат" in s)
        if th:
            td = th.find_next_sibling("td")
            if td and td.text.strip().isdigit():
                rooms = int(td.text.strip())

    # 3. Якщо взагалі не знайдено — ставимо дефолт і попереджаємо
    if rooms is None:
        print("❌ Не вдалося визначити кількість кімнат, ставимо 1")
        rooms = 1

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
        try:
            image_bytes = urlopen(data["main_image"], timeout=10).read()
            filename = f"{uuid4().hex}.webp"
            image_content = ContentFile(image_bytes)
            image_instance = PropertyImage.objects.create(property=prop, is_main=True)
            image_instance.image.save(filename, image_content, save=True)
            print(f"✅ Saved main image: {filename}")
        except Exception as e:
            print(f"❌ Error loading main image: {data['main_image']}\n{e}")


    # Додаємо інші зображення
    for i, img_url in enumerate(data["gallery"]):
        try:
            response = urlopen(img_url)
            content_type = response.info().get_content_type()
            if not content_type.startswith("image"):
                logger.warning(f"⚠️ Skipping non-image URL: {img_url} (type: {content_type})")
                continue
            file_name = basename(img_url.split("?")[0]) or f'image-{i}.jpg'
            image_file = ContentFile(response.read())
            image_instance = PropertyImage(property=prop, is_main=(i == 0))
            image_instance.image.save(file_name, image_file, save=True)
            logger.info(f"✅ Saved gallery image: {file_name}")
        except Exception as e:
            logger.error(f"❌ Error loading image: {img_url}\n{e}")


    return prop
