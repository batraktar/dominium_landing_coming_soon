from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from landing_doominium_real_state.views import SearchFiltersView, consultation_view

from landing_doominium_real_state import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.base, name='start_page'),
                  path('search/', SearchFiltersView.as_view(), name='property_search'),
                  path('landing/', views.landing, name='landing'),
                  path('admin-panel/', include('house.urls_admin_panel')),
                  path('property/<int:pk>/', views.property_detail, name='property_detail'),
                  path("consultation/", consultation_view, name="consultation"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:  # Додаємо підтримку медіафайлів у режимі розробки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
