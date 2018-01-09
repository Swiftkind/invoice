from django.db import models
from clients.models import Client
from items.models import Item

# Create your models here.
class SalesPerson(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255, unique=False, null=True, blank=True)

class Tax(models.Model):
	tax_name = models.CharField(max_length=255)
	rate = models.CharField(max_length=255)
	compound = models.BooleanField()

class ItemDetail(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quality = models.CharField(max_length=255, null=True, blank=True)
	rate = models.CharField(max_length=255, null=True, blank=True)
	tax = models.ForeignKey(Tax, on_delete=models.CASCADE,  null=True, blank=True)
	amount = models.CharField(max_length=255, null=True, blank=True)
	sub_total = models.CharField(max_length=255, null=True, blank=True)
	discount = models.CharField(max_length=255, null=True, blank=True)
	shipping_charges = models.CharField(max_length=255, null=True, blank=True)
	adjustment = models.CharField(max_length=255, null=True, blank=True)
	total = models.CharField(max_length=255, null=True, blank=True)

class Payment(models.Model):
	payment_options = models.CharField(max_length=255, null=True, blank=True)
	customer_notes = models.CharField(max_length=255, null=True, blank=True)
	term_condition = models.CharField(max_length=255, null=True, blank=True)

class Invoice(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	invoice_no = models.CharField(max_length=255, null=True, blank=True)
	order_no = models.CharField(max_length=255, null=True, blank=True)
	invoice_date = models.DateField(max_length=255, null=True, blank=True)
	terms = models.CharField(max_length=255, null=True, blank=True)
	due_date = models.DateField(max_length=255, null=True, blank=True)
	sales_person = models.ForeignKey(SalesPerson, on_delete=models.CASCADE,  null=True, blank=True)
	item_detail = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE , null=True, blank=True)
