from django.db import models
from django.utils import timezone
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from users.models import Company
from django.core.validators import MaxLengthValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import  PermissionsMixin


class Client(models.Model):

	
	owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='client', default='')
	company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
	invoiced = models.BooleanField(default=False) 
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	display_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	mobile = PhoneNumberField(null=True, blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	
	class Meta:
		unique_together = (("display_name", "owner"), ("email","owner"),)

	def __str__(self):
		return '{}'.format(self.display_name)