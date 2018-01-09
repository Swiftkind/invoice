from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', include('accounts.urls')),
    path('', include('clients.urls')),
    path('', include('items.urls')),
    path('', include('invoice.urls')),
]
