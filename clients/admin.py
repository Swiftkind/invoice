from django.contrib import admin
from clients.models import *
# Register your models here.

admin.site.register(Client)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(AdditionalAddress)

