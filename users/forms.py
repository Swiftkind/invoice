from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.conf import settings


from users.models import Company, User
from users.models import get_company_directory



class SignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    

    class Meta:
        model = User
        fields = ('email', 'confirm_password', 'first_name', 'last_name', 'middle_name', 'password')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', '')
        self.initial['email'] = ''

    def clean_confirm_password(self):
        cleaned_data = super(SignupForm, self).clean()
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("password did not match")
        return confirm_password

    def save(self, commit=False):
        instance = super(SignupForm, self).save(commit=False)
        instance.set_password(self.data.get('password'))
        if commit:
            instance.save()
        return instance



class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('city', 'logo', 'name', 'province','street')



class SigninForm(forms.Form):
    email = forms.CharField(max_length=30, widget=forms.TextInput)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    error_msg = "Email/Password is incorrect."

    def clean(self):
        """ validate user's credentials
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not (email or password):
            raise forms.ValidationError(self.error_msg, code='invalid_login')
        # check if user's credentials are valid
        self.user_cache = authenticate(email=email, password=password)
        if self.user_cache is None or \
            not self.user_cache.is_active:
            raise forms.ValidationError(self.error_msg, code='invalid_login')
        return self.cleaned_data



class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('avatar', 'email', 'first_name', 'middle_name', 'last_name')

    def clean_avatar(self):
        return self.cleaned_data['avatar']

