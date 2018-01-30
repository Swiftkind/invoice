from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from users.models import User, Company
from django.conf import settings
from users.models import get_company_directory


class SignupForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	

	class Meta:
		model = User
		fields = ('email','password','confirm_password', 'name', 'avatar')

	def __init__(self, *args, **kwargs):
		
		self.user = kwargs.pop('user', '')
		super(SignupForm, self).__init__(*args, **kwargs)
		self.initial['email'] = ''

	def clean_confirm_password(self):
		cleaned_data = super(SignupForm, self).clean()
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password != confirm_password:
			raise forms.ValidationError("password did not match")
		return confirm_password

	def clean_email(self):
		getclean_email = self.cleaned_data['email']
		if self.user:
			return getclean_email
		if self.user == '':
			emails = User.objects.filter(email=getclean_email)
			if len(emails) != 0:
				raise forms.ValidationError("Sorry but the email is already taken")
		return getclean_email

	def save(self, commit=True):
		instance = super(SignupForm, self).save(commit=False)
		instance.set_password(self.cleaned_data['password'])
		instance.save()
		return instance



class CompanyForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ('company_name','logo','city','province','street')

	def save(self,commit=True, user=None):
		instance = super(CompanyForm, self).save(commit=False)
		instance.save()
		return instance



class SigninForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())

	def clean(self):
		cleaned_data = super(SigninForm, self).clean()
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		self.auth = authenticate(email=email, password=password)
		if not self.auth:
			raise forms.ValidationError("Wrong Email or Password")
		else:
			self.user = self.auth
		return self.cleaned_data

	def clean_email(self):
		email = self.cleaned_data['email']
		if email:
			test_email = User.objects.all().filter(email__iexact=email)
			if not test_email:
				raise forms.ValidationError("No such email")
			else:
				return email
		return email


class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('email','name','avatar')

	def clean_avatar(self):
		return self.cleaned_data['avatar']



class SubUserAddForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())

	def clean_confirm_password(self):
		cleaned_data = super(SubUserAddForm, self).clean()
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password != confirm_password:
			raise forms.ValidationError("password did not match")
		return confirm_password
	
	def clean_email(self):
		getclean_email = self.cleaned_data['email']

		emails = User.objects.filter(email=getclean_email)
		if len(emails) != 0:
			raise forms.ValidationError("Sorry but the email is already taken")
		return getclean_email
