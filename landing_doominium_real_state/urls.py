from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from landing_doominium_real_state.views import SearchFiltersView, consultation_view, toggle_like, liked_properties_view

from landing_doominium_real_state import views

urlpatterns = [
                path('', include('accounts.urls')),
                path('admin/', admin.site.urls),
                path('', views.base, name='start_page'),
                path('search/', SearchFiltersView.as_view(), name='property_search'),
                path('signup/', views.signup, name='landing'),
                path('admin-panel/', include('house.urls_admin_panel')),
                path('property/<slug:slug>/', views.property_detail, name='property_detail'),
                path("consultation/", consultation_view, name="consultation"),
                path('like/<int:property_id>/', toggle_like, name='toggle_like'),
                path('likes/', liked_properties_view, name='liked_properties'),
            ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:  # Додаємо підтримку медіафайлів у режимі розробки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
