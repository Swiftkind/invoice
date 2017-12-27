from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password

from accounts.models import Account

class SignupForm(forms.ModelForm):
	""" 
	Signup form
	"""
	email = forms.EmailField(widget=forms.EmailInput({'class': 'form-control', 'placeholder': 'Email address'}))
	password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control', 'placeholder': 'Password'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control', 'placeholder': 'Confirm Password'}))

	class Meta:
		model = Account
		fields = ('email','password','confirm_password')

	def clean_confirm_password(self):
		'''
		checks if the password is matched
		'''
		cleaned_data = super(SignupForm, self).clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')

		if password != confirm_password:
			raise forms.ValidationError("password dit not match")
		return confirm_password


	def clean_email(self):
		""" 
		Checks if the email is already taken
		"""
		getclean_email = self.cleaned_data['email']
		emails = Account.objects.filter(email=getclean_email)
		if len(emails) != 0:
			raise forms.ValidationError("Sorry but the Email is already TAKEN")
		return getclean_email

	def save(self, commit=True):
		""" 
		Saves the user data
		"""
		instance = super(SignupForm, self).save(commit=False)
		instance.set_password(self.cleaned_data['password'])
		instance.save()
		return instance


class SigninForm(forms.Form):
	"""
	Signin form
	"""
	email = forms.EmailField(widget=forms.EmailInput({'class': 'form-control', 'placeholder': 'Email address'}))
	password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control', 'placeholder': 'Password'}))

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		"""
		Get data from to authenticate
		"""
		cleaned_data = super(SigninForm, self).clean()
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		self.auth = authenticate(email=email, password=password)
		if not self.auth:
			raise forms.ValidationError("Wrong Email or Password")
		else:
			self.user = self.auth
		return self.cleaned_data