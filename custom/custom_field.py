from django.forms import *
from django.db.models.fields import *
from custom.choices import *
from custom.custom_widget import *


class SalutationField(ChoiceField):
	widget = SelectWithDisabled
	def __init__(self, *args, **kwargs):
		super(SalutationField, self).__init__(*args, **kwargs)
		self.choices = SALUTATION


class CustomModelSalutationField(CharField):
	def formfield(self, **kwargs):
		# Passing max_length to forms.CharField means that the value's length
		# will be validated twice. This is considered acceptable since we want
		# the value in the form field (to pass into widget for example).
		defaults = {'max_length': self.max_length}
		if not self.choices:
			defaults['widget'] = SelectWithDisabled
		defaults.update(kwargs)
		return super().formfield(**defaults)


