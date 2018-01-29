from django.forms import (	ValidationError, 
							ModelForm, 
							Form, 
							EmailField, 
							CharField,
							ChoiceField,
							URLField, 
							EmailInput, 
							PasswordInput,
							TextInput,
						)
from clients.models import Client
from django.core.validators import URLValidator, MinLengthValidator

from django.core.validators import MaxLengthValidator
from django.conf import settings
from django.forms.utils import  ErrorList



class ClientForm(ModelForm):

	
	class Meta:
		model = Client
		fields = ('display_name','first_name',  'last_name','email','mobile')

	def __init__(self,*args, **kwargs):
		#import pdb; pdb.set_trace()
		self.user = kwargs.pop('user', None)
		return super(ClientForm, self).__init__(*args, **kwargs)

	def clean_display_name(self):
		#import pdb; pdb.set_trace()
		display_name = self.cleaned_data['display_name']
		if display_name:
				test_display_name = Client.objects.filter(display_name__exact=display_name, owner__exact=self.user)
				if test_display_name.exists():
					raise ValidationError("name already exists")
		return display_name

	def clean_email(self):
		email = self.cleaned_data['email']
		if email:
			test_email = Client.objects.filter(email__exact=email, owner__exact=self.user)
			if test_email.exists():
				raise ValidationError("email already used by other client")
		return email

	def clean_mobile(self):
		mobile = self.cleaned_data['mobile']
		if mobile:
			test_mobile = Client.objects.filter(mobile__exact=mobile, owner__exact=self.user)
			if test_mobile.exists():
				raise ValidationError("mobile already used by other client")
		return mobile

	def save(self, commit=True):
		#import pdb; pdb.set_trace()
		instance = super(ClientForm, self).save(commit=False)
		instance.owner = self.user
		#contact = Client(**self.cleaned_data)
		if commit:
			instance.save()
		return instance


