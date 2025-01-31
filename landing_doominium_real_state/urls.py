from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from landing_doominium_real_state import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('action_for_owners', views.action_for_owners, name='action_for_owners')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
