from django.contrib import admin
from contacts.models import Contact, ShippingAddress, BillingAddress, AdditionalAddress, ContactPerson, AddMoreField
# Register your models here.

admin.site.register(Contact)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(AdditionalAddress)
admin.site.register(AddMoreField)
admin.site.register(ContactPerson)
