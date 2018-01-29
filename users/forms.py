from django.forms import (	ValidationError, 
							ModelForm, 
							Form, 
							EmailField, 
							CharField, 
							EmailInput, 
							PasswordInput,
							TextInput,
						)
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from users.models import User
from django.conf import settings
from users.models import get_company_directory


class SignupForm(ModelForm):
	email = EmailField(widget=EmailInput())
	password = CharField(widget=PasswordInput())
	confirm_password = CharField(widget=PasswordInput())
	

	class Meta:
		model = User
		fields = ('email','password','confirm_password', 'name','province', 'city', 'street','logo','company')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.initial['email'] = ''
		self.initial['name'] = ''
		self.user = kwargs.pop('user', '')
		self.logo = kwargs.pop('logo', '')

	def clean_logo(self):	
		return self.cleaned_data['logo']

	def clean_confirm_password(self):
		cleaned_data = super(SignupForm, self).clean()
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password != confirm_password:
			raise ValidationError("password did not match")
		return confirm_password

	def clean_email(self):
		getclean_email = self.cleaned_data['email']
		if self.user:
			return getclean_email
		if self.user == '':
			emails = User.objects.filter(email=getclean_email)
			if len(emails) != 0:
				raise ValidationError("Sorry but the email is already taken")
		return getclean_email

	def save(self, commit=True):
		instance = super(SignupForm, self).save(commit=False)
		instance.set_password(self.cleaned_data['password'])
		#if self.user:
		#	instance.logo = self.logo
		
		instance.save()
		return instance



class SigninForm(Form):
	email = EmailField(widget=EmailInput())
	password = CharField(widget=PasswordInput())

	def clean(self):
		cleaned_data = super(SigninForm, self).clean()
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		self.auth = authenticate(email=email, password=password)
		if not self.auth:
			raise ValidationError("Wrong Email or Password")
		else:
			self.user = self.auth
		return self.cleaned_data

	def clean_email(self):
		email = self.cleaned_data['email']
		if email:
			test_email = User.objects.all().filter(email__iexact=email)
			if not test_email:
				raise ValidationError("No such email")
			else:
				return email
		return email


class UserUpdateForm(ModelForm):


	class Meta:
		model = User
		fields = ('email','name','avatar', 'street', 'city', 'province','logo','company')

	def clean_avatar(self):
		return self.cleaned_data['avatar']



class SubUserAddForm(Form):
	email = EmailField(widget=EmailInput())
	password = CharField(widget=PasswordInput())
	confirm_password = CharField(widget=PasswordInput())

	def clean_confirm_password(self):
		cleaned_data = super(SubUserAddForm, self).clean()
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password != confirm_password:
			raise ValidationError("password did not match")
		return confirm_password
	
	def clean_email(self):
		getclean_email = self.cleaned_data['email']

		emails = User.objects.filter(email=getclean_email)
		if len(emails) != 0:
			raise ValidationError("Sorry but the email is already taken")
		return getclean_email
