
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('clients.urls')),
    path('', include('invoices.urls')),
    path('', include('items.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
