from django.db import models
from django.utils.safestring import mark_safe
from geopy.geocoders import Nominatim


class PropertyType(models.Model):
    name = models.CharField(max_length=50)

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
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True)
    deal_type = models.ForeignKey(DealType, on_delete=models.SET_NULL, null=True, blank=True)
    features = models.ManyToManyField(Feature, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.address and (self.latitude is None or self.longitude is None):
            geolocator = Nominatim(user_agent="dominium")
            location = geolocator.geocode(self.address)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
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
        # Автоматично скидає попереднє головне фото
        if self.is_main:
            PropertyImage.objects.filter(property=self.property, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
