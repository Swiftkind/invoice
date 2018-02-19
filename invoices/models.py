from django.db import models
from django.conf import settings

from items.models import Item
from clients.models import Client
from users.models import User, Company
from invoices.utils import get_invoice_directory



class Invoice(models.Model):
    '''creating database for invoice
    '''
    DRAFT = 'draft'
    SENT = 'sent'
    
    STATUS = (
        (DRAFT, 'Draft'),
        (SENT, 'Sent'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='invoice', default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    client  = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    
    invoice_number = models.PositiveIntegerField()
    invoice_date = models.DateField()
    due_date = models.DateField()
    
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    remarks = models.TextField(max_length=255,null=True, blank=True)
   
    pdf = models.FileField(upload_to=get_invoice_directory,null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    payment_status = models.BooleanField( default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("invoice_number", "company"),)

    def __str__(self):
        return f"{self.invoice_number}"

    def get_invoice_number(self):
        return f"{self.invoice_number}".zfill(9)







