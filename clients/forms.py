from django.forms import *
from custom.custom_widget import *
from clients.models import *

class ShippingAddressForm(ModelForm):
	class Meta:
		model = ShippingAddress
		fields = '__all__'

class BillingAddressForm(ModelForm):
	class Meta:
		model = BillingAddress
		fields = '__all__'

class AdditionalAddressForm(ModelForm):
	class Meta:
		model = AdditionalAddress
		fields = '__all__'

class ClientForm(ModelForm):
	class Meta:
		model = Client
		exclude = ['billing_address', 'shipping_address', 'additional_address',]

	'''
	def save(self, commit=True):

		if commit:
			contact = super(ClientForm, self).save(commit=False)
			print('jojo')
			print(contact)
			#billing = BillingAddressForm().save()
			#contact.billing_address = billing

			contact.save()
			print('hehe --')
			print(contact)
		return contact
	'''



	'''
	def save(self, commit=True):
		#import pdb; pdb.set_trace()
		""" 
		Saves the user data
		"""
		contact = super(ContactForm, self).save(commit=False)
		#billing = BillingAddressForm().save()
		#contact.billing_address = billing

		contact.save()
		return contact
	'''


	'''
	def save(self, commit=True, *args, **kwargs):
		#import pdb; pdb.set_trace()
		contact = super(ContactForm, self).save(commit=False)
		contact.salutation    = self.cleaned_data['salutation']
		contact.first_name    = self.cleaned_data['first_name']
		contact.last_name     = self.cleaned_data['last_name']
		contact.email_address = self.cleaned_data['email_address']
		contact.work_phone    = self.cleaned_data['work_phone']
		contact.mobile        = self.cleaned_data['mobile']
		contact.contact_display_name = self.cleaned_data['contact_display_name']
		contact.company_name  = self.cleaned_data['company_name']
		contact.website       = self.cleaned_data['website']
		contact.currency      = self.cleaned_data['currency']
		contact.payment_terms = self.cleaned_data['payment_terms']
		contact.portal        = self.cleaned_data['portal']
		contact.portal_language = self.cleaned_data['portal_language']
		contact.facebook      = self.cleaned_data['facebook']
		contact.twitter      = self.cleaned_data['twitter']
		contact.remarks      = self.cleaned_data['remarks']

		contact.save()
		return contact
	'''



	
	
