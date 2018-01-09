from django.forms import Form,ModelForm, TextInput, ChoiceField, Select
from clients.models import *
from invoice.models import Invoice,Payment,ItemDetail

class CustomerForm(ModelForm):
	class Meta:
		model = Invoice
		exclude = ['payment', 'item_detail']

class PaymentForm(ModelForm):
	class Meta:
		model = Payment
		fields = '__all__'

class ItemDetailForm(ModelForm):
	class Meta:
		model = ItemDetail
		fields = '__all__'
