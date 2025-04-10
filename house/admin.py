from django.contrib import admin
from django.utils.html import format_html

from .models import Property, PropertyImage, PropertyType, DealType, Feature


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(DealType)
class DealTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name']


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    max_num = 10
    fields = ['image', 'is_main', 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ['title', 'address', 'price']
    exclude = ['latitude', 'longitude']
    filter_horizontal = ['features']  # ← для зручного вибору множинних features


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'is_main']
