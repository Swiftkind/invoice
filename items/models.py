from django.db import models
from django.db import models
from django.conf import settings


from clients.models import Client
from users.models import User, Company



class Item(models.Model):
    FIXED = 'fixed'
    QUANTITY = 'quantity'
    INVOICE_TYPE = (
        (FIXED, 'Fixed Price'),
        (QUANTITY, 'Quantity'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='items', default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='item_company')
    invoiced = models.BooleanField(default=False) 
    item_type = models.CharField(max_length=10,choices=INVOICE_TYPE, default='fixed')
    order_number = models.PositiveIntegerField( null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True) 
    rate = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    total_amount = models.PositiveIntegerField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_number}"

    def total(self):
        return self.rate*self.quantity