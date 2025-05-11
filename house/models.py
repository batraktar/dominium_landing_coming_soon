import json
import random
import uuid
import os
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.urls import reverse
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from geopy.geocoders import Nominatim 


class PropertyType(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # якщо такий slug вже існує — додаємо "-1", "-2" і т.д.
            original_slug = self.slug
            counter = 1
            while PropertyType.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    
class DealType(models.Model):
    name = models.CharField(max_length=50)  # Наприклад: Оренда / Продаж

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=4569)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    property_type = models.ForeignKey('PropertyType', on_delete=models.SET_NULL, null=True, blank=True)
    deal_type = models.ForeignKey('DealType', on_delete=models.SET_NULL, null=True, blank=True)
    features = models.ManyToManyField('Feature', blank=True)

    slug = models.SlugField(unique=True, blank=True)

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    # Генерація slug, де замість ID використовується хеш (6 символів із UUID)
    def generate_semantic_slug(self):
        suffix = uuid.uuid4().hex[:6]
        return slugify(f"{self.city}-{self.address}-{self.rooms}k-{suffix}")

    def generate_data_driven_slug(self):
        suffix = uuid.uuid4().hex[:6]
        return slugify(f"{self.title}-{self.address}-{int(self.price)}usd-{suffix}")

    def generate_branded_slug(self):
        brand_tokens = [
            "estate", "capital", "vista", "prime", "terra",
            "urbis", "noble", "domus", "valley", "atlas"
        ]
        word = random.choice(brand_tokens)
        suffix = uuid.uuid4().hex[:6]
        return slugify(f"dominium-{self.title}-{word}-{suffix}")

    def save(self, *args, **kwargs):
        creating = self.pk is None  # Чи об'єкт щойно створюється

        # Автоматична генерація координат
        if self.address and (self.latitude is None or self.longitude is None):
            try:
                geolocator = Nominatim(user_agent="dominium")
                location = geolocator.geocode(self.address)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except Exception as e:
                print("⚠️ Geocode error:", e)

        # Генеруємо slug, якщо він ще не встановлений
        if not self.slug:
            slug_generators = [
                self.generate_semantic_slug,
                self.generate_data_driven_slug,
                self.generate_branded_slug,
            ]
            base_slug = random.choice(slug_generators)()
            slug = base_slug
            n = 1
            # Перевірка на унікальність slug у базі
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug

        # Фінальне збереження
        super().save(*args, **kwargs)


    @property
    def images_json(self):
        """Список URL всіх зображень (використовують JS-галереї)."""
        return mark_safe(json.dumps([img.image.url for img in self.images.all()]))

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.property.title}"

    def save(self, *args, **kwargs):
        # Обнуляємо попереднє головне фото
        if self.is_main:
            PropertyImage.objects.filter(property=self.property, is_main=True).update(is_main=False)

        # --- Конвертація в WebP ---
        if self.image and not self.image.name.endswith('.webp'):
            self.image = self.convert_to_webp(self.image)

        super().save(*args, **kwargs)

    def convert_to_webp(self, image_field):
        img = Image.open(image_field)
        img = img.convert('RGB')  # WebP не підтримує альфа-канал

        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=85)

        name_base = os.path.splitext(image_field.name)[0]
        webp_name = f"{name_base}.webp"

        return ContentFile(buffer.getvalue(), name=webp_name)
    
    