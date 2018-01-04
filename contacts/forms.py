from django.forms.utils import ErrorList
from django.utils.translation import gettext as _
from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
from django.forms.models import model_to_dict
from django.forms import (	
							Form,
							CharField,
							EmailField,
							BooleanField,
							EmailInput,
							ChoiceField,
							ModelForm,
							TextInput,
							Textarea,
							EmailInput,
							URLInput,
							URLField,
							Select,
							CheckboxInput,
							formset_factory
						 )

from contacts.models import (
								Contact, 
								AddMoreField,
								ContactPerson,
								BillingAddress, 
								ShippingAddress, 
								AdditionalAddress, 
							)

from contacts.choices import SALUTATION, CURRENCY, PAYMENT_TERMS
from languages.fields import LanguageField
from languages.languages import LANGUAGES
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django_countries.fields import LazyTypedChoiceField
from django_countries.data import COUNTRIES
from django.utils.translation import gettext_lazy as _

class AddressForm(Form):
	attention = CharField(max_length=40 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Attention'}))
	street_1  = CharField(max_length=100 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Street 1'}))
	street_2  = CharField(max_length=100 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Street 2'}))
	city      = CharField(max_length=60 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
	country   = LazyTypedChoiceField(required=False, widget=Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),choices=COUNTRIES)
	state     = CharField(max_length=30 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
	zip_code  = CharField(max_length=16 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}))
	phone     = CharField(max_length=18 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
	fax       = CharField(max_length=15 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'fax'}))
		

class CommonContactInfoForm(Form):
	salutation    = ChoiceField(required=False, widget=Select(attrs={'class': 'form-control', 'placeholder': 'Salutation'}), choices=SALUTATION) 
	first_name    = CharField(max_length=40 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
	last_name     = CharField(max_length=40 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
	email_address = EmailField(max_length=255 , required=False ,widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
	work_phone    = CharField(max_length=18 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Work Phone'}))
	mobile        = CharField(max_length=12 , required=False ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile'}))


class AddMoreFieldForm(Form):
	skype_account = CharField(max_length=100 ,required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Skype Account'}))
	designation   = CharField(max_length=100 ,required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}))
	department    = CharField(max_length=100 ,required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}))

	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
						initial=None, error_class=ErrorList, label_suffix=None,
						empty_permitted=False, instance=None, use_required_attribute=None):
		opts = AddMoreFiel()
		if opts is None:
			raise ValueError('ModelForm has no model class specified.')
		if instance is None:
			# if we didn't get an instance, instantiate a new one
			self.instance = opts
			object_data = {}
		else:
			self.instance = instance
			object_data = model_to_dict(instance)
		if prefix is not None:
			self.prefix = prefix
		super(AddMoreFieldForm, self).__init__(
											data, files, auto_id, prefix, object_data, error_class,
											label_suffix, empty_permitted, use_required_attribute=use_required_attribute,
										)

class ContactPersonForm(CommonContactInfoForm):
	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
						initial=None, error_class=ErrorList, label_suffix=None,
						empty_permitted=False, instance=None, use_required_attribute=None):
		opts = ContactPerson()
		if opts is None:
			raise ValueError('ModelForm has no model class specified.')
		if instance is None:
			# if we didn't get an instance, instantiate a new one
			self.instance = opts
			object_data = {}
		else:
			self.instance = instance
			object_data = model_to_dict(instance)
		if prefix is not None:
			self.prefix = prefix
		super(ContactPersonForm, self).__init__(
											data, files, auto_id, prefix, object_data, error_class,
											label_suffix, empty_permitted, use_required_attribute=use_required_attribute,
										)

class ShippingAddressForm(AddressForm):
	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
						initial=None, error_class=ErrorList, label_suffix=None,
						empty_permitted=False, instance=None, use_required_attribute=None):
		opts = ShippingAddress()
		if opts is None:
			raise ValueError('ModelForm has no model class specified.')
		if instance is None:
			# if we didn't get an instance, instantiate a new one
			self.instance = opts
			object_data = {}
		else:
			self.instance = instance
			object_data = model_to_dict(instance)
		if prefix is not None:
			self.prefix = prefix
		super(ShippingAddressForm, self).__init__(
											data, files, auto_id, prefix, object_data, error_class,
											label_suffix, empty_permitted, use_required_attribute=use_required_attribute,
										)
        
class BillingAddressForm(AddressForm):
	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
						initial=None, error_class=ErrorList, label_suffix=None,
						empty_permitted=False, instance=None, use_required_attribute=None):
		opts = BillingAddress()
		if opts is None:
			raise ValueError('ModelForm has no model class specified.')
		if instance is None:
			# if we didn't get an instance, instantiate a new one
			self.instance = opts
			object_data = {}
		else:
			self.instance = instance
			object_data = model_to_dict(instance)
		if prefix is not None:
			self.prefix = prefix
		super(BillingAddressForm, self).__init__(
											data, files, auto_id, prefix, object_data, error_class,
											label_suffix, empty_permitted, use_required_attribute=use_required_attribute,
										)
        
class AdditionalAddressForm(AddressForm):
	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
						initial=None, error_class=ErrorList, label_suffix=None,
						empty_permitted=False, instance=None, use_required_attribute=None):
		opts = AdditionalAddress()
		if opts is None:
			raise ValueError('ModelForm has no model class specified.')
		if instance is None:
			# if we didn't get an instance, instantiate a new one
			self.instance = opts
			object_data = {}
		else:
			self.instance = instance
			object_data = model_to_dict(instance)
		if prefix is not None:
			self.prefix = prefix
		super(AdditionalAddressForm, self).__init__(
											data, files, auto_id, prefix, object_data, error_class,
											label_suffix, empty_permitted, use_required_attribute=use_required_attribute,
										)
        
class ContactForm(CommonContactInfoForm):
	company_name          = CharField(max_length=255 , required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}))
	contact_display_name  = CharField(max_length=255 , required=True, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Display Name'}))
	website               = URLField(max_length=100 , required=False, widget=URLInput(attrs={'class': 'form-control', 'placeholder': 'Website'}))

	currency              = ChoiceField(required=False, widget=Select(attrs={'class': 'form-control', 'placeholder': 'Currency'}), choices=CURRENCY)
	payment_terms         = ChoiceField(required=False, widget=Select(attrs={'class': 'form-control', 'placeholder': 'Payment Terms'}),choices=PAYMENT_TERMS)
	portal                = BooleanField(required=False,widget=CheckboxInput())
	portal_language       = ChoiceField(required=False, widget=Select(attrs={'class': 'form-control', 'placeholder': 'Language'}), choices=LANGUAGES)
	facebook              = CharField(max_length=100 , required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook'}))
	twitter               = CharField(max_length=100 , required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter'}))
	remarks               = CharField(max_length=500 , required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Remark'}))


	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
						initial=None, error_class=ErrorList, label_suffix=None,
						empty_permitted=False, instance=None, use_required_attribute=None):
		opts = Contact()
		if opts is None:
			raise ValueError('ModelForm has no model class specified.')
		if instance is None and prefix is not None:
			# if we didn't get an instance, instantiate a new one
			self.instance = opts
			self.prefix = prefix
			object_data = {}
		else:
			self.instance = instance
			object_data = model_to_dict(instance)
		super(ContactForm, self).__init__(
											data, files, auto_id, prefix, object_data, error_class,
											label_suffix, empty_permitted, use_required_attribute=use_required_attribute,
										)

	
