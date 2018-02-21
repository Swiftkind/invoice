from django.contrib import admin
from invoices.models import Invoice, Item


class ItemInline(admin.TabularInline):
    model = Item

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ItemInline]


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Item)