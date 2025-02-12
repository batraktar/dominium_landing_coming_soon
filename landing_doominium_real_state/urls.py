from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from landing_doominium_real_state.views import consultation_view

from landing_doominium_real_state import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('consultation/', consultation_view, name="consultation"),
    path('base/', views.base, name='start_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "landing_doominium_real_state.views.custom_404"
