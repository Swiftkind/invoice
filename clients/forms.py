from django import forms
from clients.models import Client



class ClientForm(forms.ModelForm):
    ''' Form for creating Client
    '''
    class Meta:
        model = Client
        fields = ('display_name','email','first_name','last_name','mobile')


    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user', None)
        return super(ClientForm, self).__init__(*args, **kwargs)


    def clean_display_name(self):
        '''for unique validation in display_name
        '''
        display_name = self.cleaned_data['display_name']
        if display_name:
                test_display_name = Client.objects.filter(display_name__exact=display_name, company__exact=self.user.company)
                if test_display_name.exists():
                    raise forms.ValidationError("name already exists")
        return display_name


    def clean_email(self):
        '''for unique validation in email
        '''
        email = self.cleaned_data['email']
        if email:
            test_email = Client.objects.filter(email__exact=email, company__exact=self.user.company)
            if test_email.exists():
                raise forms.ValidationError("email already used by other client")
        return email


    def clean_mobile(self):
        '''for unique validation in mobile
        '''
        mobile = self.cleaned_data['mobile']
        if mobile:
            test_mobile = Client.objects.filter(mobile__exact=mobile, company__exact=self.user.company)
            if test_mobile.exists():
                raise forms.ValidationError("mobile already used by other client")
        return mobile


    def save(self, commit=True, company=None):
        instance = super(ClientForm, self).save(commit=False)
        instance.owner = self.user
        instance.company = company
        instance.save()
        return instance


