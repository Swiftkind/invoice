from django.db.models import ( 	OneToOneField,
								Model,
								ForeignKey, 
								CASCADE, 
								EmailField,
								CharField,
								DateTimeField, 
								BooleanField, 
								ImageField,
								TextField,
								PositiveIntegerField,
								BigAutoField,
								DateField,
								TimeField,
								FileField
								
							)
from django.utils import timezone
from clients.models import Client
from custom.choices import INVOICE_TYPE, STATUS
from users.models import User
from django.conf import settings
from django.contrib.auth.models import  PermissionsMixin
from invoices.utils import get_invoice_directory



class Invoice(Model):

	owner = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE, related_name='invoice', default='')
	client  = ForeignKey(Client, on_delete=CASCADE)
	order_number = PositiveIntegerField()
	invoice_number = PositiveIntegerField()
	invoice_date = DateField()
	due_date = DateField()
	invoice_type = CharField(max_length=10,choices=INVOICE_TYPE, default='fixed')
	rate = PositiveIntegerField(null=True, blank=True)
	hours = PositiveIntegerField(null=True, blank=True)
	start_time = TimeField(null=True, blank=True)
	end_time = TimeField(null=True, blank=True)
	amount = PositiveIntegerField(null=True, blank=True)
	status = CharField(max_length=10, default='draft')
	paid = PositiveIntegerField(default=0)
	remarks = TextField(max_length=255,null=True, blank=True)
	total_amount = PositiveIntegerField(null=True, blank=True)
	pdf = FileField(upload_to=get_invoice_directory,null=True, blank=True)

	date_created = DateTimeField(auto_now_add=True)
	date_updated = DateTimeField(auto_now=True)

	class Meta:
		unique_together = ( ("order_number","owner"), ("invoice_number","owner"),)

	def __str__(self):
		return '{}'.format(self.invoice_number)

