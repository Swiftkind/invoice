from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from users.models import User, Company
from django.conf import settings
from users.models import get_company_directory



class SignupForm(forms.ModelForm):
    """Signup form
    """
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password', 'name', 'avatar')


    def clean_confirm_password(self):
        """Confirm password checking
        """
        cleaned_data = super(SignupForm, self).clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("password did not match")
        return confirm_password


    def save(self, commit=True):
        """Create user
        """
        instance = super(SignupForm, self).save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        instance.save()
        return instance



class CompanyForm(forms.ModelForm):
    """Company data form
    """
    class Meta:
        model = Company
        fields = ('company_name', 'city', 'logo', 'province', 'street')


    def save(self,commit=True):
        instance = super(CompanyForm, self).save(commit=False)
        instance.save()
        return instance



class SigninForm(forms.Form):
    """User signin form
    """
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


    def clean(self):
        """Get sign form data and authenticate
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



class UserUpdateForm(forms.ModelForm):
    """User update form
    """
    class Meta:
        model = User
        fields = ('avatar', 'email', 'name')



class SubUserAddForm(forms.Form):
    """Subuser form
    """
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


    def clean_confirm_password(self):
        """Confirm password checking
        """
        cleaned_data = super(SubUserAddForm, self).clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("password did not match")
        return confirm_password
