from django.urls import path

from .views import import_property_by_url
from .views_admin_panel import admin_dashboard, delete_property, property_images_api, patch_property, login_view

urlpatterns = [
    path('login/', login_view, name='admin_login'),
    path("dashboard/", admin_dashboard, name="custom_admin"),
    path("import-from-url/", import_property_by_url, name="import_property_by_url"),
    path("delete/<int:pk>/", delete_property, name="delete_property"),
    path("api/property/<int:pk>/images/", property_images_api, name="property_images_api"),
    path("api/properties/<int:pk>/patch/", patch_property, name="patch_property"),

]
