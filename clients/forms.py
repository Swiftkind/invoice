from django import forms
from clients.models import Client


class ClientForm(forms.ModelForm):
    """ Form for creating Client
    """
    class Meta:
        model = Client
        fields = ('client_company', 
                  'client_company_logo', 
                  'email', 
                  'first_name', 
                  'last_name', 
                  'mobile', 
                  'middle_name', 
                  )

    def __init__(self,*args, **kwargs):
        """Client needs company for filtering
        """
        self.company = kwargs.pop('company', None)
        return super(ClientForm, self).__init__(*args, **kwargs)

    def clean_client_company(self):
        """For unique validation in client_company
        """
        client_company = self.cleaned_data['client_company']
        client_company_q = Client.objects.filter(client_company=client_company, company=self.company)
        if not self.instance:
            if client_company_q:
                raise forms.ValidationError("Display name already exists:")
        if self.instance.client_company != client_company:
            if client_company_q.exists():
                raise forms.ValidationError("Display name already exists:")
        return client_company

    def clean_mobile(self):
        """For unique validation in mobile
        """
        mobile = self.cleaned_data['mobile']
        mobile_q = Client.objects.filter(mobile__exact=mobile, company=self.company)
        if not self.instance:
            if mobile_q:
                raise forms.ValidationError("Mobile already exists:")
        if self.instance.mobile != mobile:
            if mobile_q.exists():
                raise forms.ValidationError("Mobile already exists:")
        return mobile

