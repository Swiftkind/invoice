from django.db import models

# Create your models here.
class Item(models.Model):
	item_type = models.CharField(max_length=25,null=True, blank=True)
	name = models.CharField(max_length=255)
	unit = models.CharField(max_length=255, null=True, blank=True)
	rate = models.CharField(max_length=255)
	description = models.CharField(max_length=255, null=True, blank=True)
	tax = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return '%s' % (self.name)