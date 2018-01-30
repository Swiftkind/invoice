from django.db import models
from django.utils import timezone
from clients.models import Client
from custom.choices import INVOICE_TYPE, STATUS
from users.models import User
from users.models import Company
from django.conf import settings
from django.contrib.auth.models import  PermissionsMixin
from invoices.utils import get_invoice_directory




class Invoice(models.Model):

	owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='invoice', default='')
	company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
	client  = models.ForeignKey(Client, on_delete=models.CASCADE)
	order_number = models.PositiveIntegerField()
	invoice_number = models.PositiveIntegerField()
	invoice_date = models.DateField()
	due_date = models.DateField()
	invoice_type = models.CharField(max_length=10,choices=INVOICE_TYPE, default='fixed')
	rate = models.PositiveIntegerField(null=True, blank=True)
	hours = models.PositiveIntegerField(null=True, blank=True)
	start_time = models.TimeField(null=True, blank=True)
	end_time = models.TimeField(null=True, blank=True)
	amount = models.PositiveIntegerField(null=True, blank=True)
	status = models.CharField(max_length=10, default='draft')
	paid = models.PositiveIntegerField(default=0)
	remarks = models.TextField(max_length=255,null=True, blank=True)
	total_amount = models.PositiveIntegerField(null=True, blank=True)
	pdf = models.FileField(upload_to=get_invoice_directory,null=True, blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ( ("order_number","owner"), ("invoice_number","owner"),)

	def __str__(self):
		return '{}'.format(self.invoice_number)





