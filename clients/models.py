from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from languages.fields import LanguageField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from custom.choices import *

class BaseAddress(models.Model):
	attention = models.CharField(max_length=40, null=True, blank=True, default='')
	street_1  = models.CharField(max_length=100, null=True, blank=True, default='')
	street_2  = models.CharField(max_length=100, null=True, blank=True, default='')
	city      = models.CharField(max_length=60, null=True, blank=True, default='')
	state     = models.CharField(max_length=30, null=True, blank=True, default='')
	zip_code  = models.CharField(max_length=16, null=True, blank=True, default='')
	country   = CountryField(max_length=100, null=True, blank=True, default='')
	phone     = models.CharField(max_length=18, null=True, blank=True, default='')
	fax       = models.CharField(max_length=15, null=True, blank=True, default='')

	class Meta:
		abstract = True


class AdditionalAddress(BaseAddress):
	def __str__(self):
		return '%s, %s, %s' % (self.street_1, self.city, self.country)

class BillingAddress(BaseAddress):
	def __str__(self):
		return '%s, %s, %s' % (self.street_1, self.city, self.country)
	
class ShippingAddress(BaseAddress):
	def __str__(self):
		return '%s, %s, %s' % (self.street_1, self.city, self.country)

class Client(models.Model):
	salutation          = models.CharField(max_length=4,  null=True, blank=True, choices=SALUTATION, default='')
	first_name          = models.CharField(max_length=40, null=True, blank=True, default='')
	last_name           = models.CharField(max_length=40, null=True, blank=True, default='')
	email_address       = models.EmailField(max_length=255,null=True, blank=True, unique=False)
	work_phone          = models.CharField(max_length=18, null=True, blank=True, default='')
	mobile              = models.CharField(max_length=12, null=True, blank=True, default='')
	client_display_name = models.CharField(max_length=255)
	company_name        = models.CharField(max_length=255, null=True, blank=True, default='')
	website             = models.URLField(max_length=100,  null=True, blank=True, default='')
	skype_account       = models.CharField(max_length=100, null=True, blank=True, default='')
	designation         = models.CharField(max_length=100, null=True, blank=True, default='')
	department          = models.CharField(max_length=100, null=True, blank=True, default='')
	currency            = models.CharField(max_length=10,  null=True, choices=CURRENCY, default='')
	payment_terms       = models.CharField(max_length=40,  null=True, blank=True, choices=PAYMENT_TERMS, default='')
	portal              = models.BooleanField(default=False)
	portal_language     = LanguageField(max_length=40,     null=True, blank=True, default='')
	facebook            = models.CharField(max_length=100, null=True, blank=True, default='')
	twitter             = models.CharField(max_length=100, null=True, blank=True, default='')
	remarks             = models.TextField(max_length=500, null=True, blank=True, default='')

	billing_address     = models.ForeignKey(BillingAddress,   on_delete=models.CASCADE, null=True, blank=True)
	shipping_address    = models.ForeignKey(ShippingAddress,  on_delete=models.CASCADE, null=True, blank=True)
	additional_address  = models.ForeignKey(AdditionalAddress,on_delete=models.CASCADE,null=True, blank=True)
	

	#class Meta:
	#	ordering = ["-email_address"]
	#	unique_together = (('email_address','contact_person.email_address'),)

	@property
	def full_name(self):
		return '%s %s' % (self.first_name,self.last_name)

	
	def __str__(self):
		return self.client_display_name



	