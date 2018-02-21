from django.conf import settings
from django.db import models


from clients.models import Client
from users.models import User, Company
from invoices.utils import get_invoice_directory


class Invoice(models.Model):
    """ Creating database for invoice
    """
    DRAFT = 'draft'
    SENT = 'sent'
    
    STATUS = (
        (DRAFT, 'Draft'),
        (SENT, 'Sent'),
    )
    archive = models.BooleanField(default=False)
    client  = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    due_date = models.DateField()
    invoice_number = models.PositiveIntegerField()
    invoice_date = models.DateField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, 
                              related_name='invoice', 
                              default=''
                              )
    payment_status = models.BooleanField( default=False)
    pdf = models.FileField(upload_to=get_invoice_directory,null=True, blank=True)
    remarks = models.TextField(max_length=255,null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='draft')

    class Meta:
        unique_together = ('invoice_number', 'company')

    def __str__(self):
        return f"{self.invoice_number}".zfill(9)


class Item(models.Model):
    """ Item form
    """
    amount = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, 
                              related_name='items', 
                              default=''
                              )
    quantity = models.PositiveIntegerField()
    rate = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.description}"
