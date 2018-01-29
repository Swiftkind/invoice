from django.db.models import PositiveIntegerField, Model,ForeignKey, CASCADE, EmailField,CharField,DateTimeField, BooleanField, ImageField,TextField
from django.utils import timezone
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
#from invoices.models import Invoice
from django.core.validators import MaxLengthValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import  PermissionsMixin


class Client(Model):

	
	owner = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE, related_name='client', default='')
	invoiced = BooleanField(default=False) 
	first_name = CharField(max_length=50)
	last_name = CharField(max_length=50)
	display_name = CharField(max_length=100)
	email = EmailField(max_length=255)
	mobile = PhoneNumberField(null=True, blank=True)

	date_created = DateTimeField(auto_now_add=True)
	date_updated = DateTimeField(auto_now=True)

	
	class Meta:
		unique_together = (("display_name", "owner"), ("email","owner"),)

	def __str__(self):
		return '{}'.format(self.display_name)