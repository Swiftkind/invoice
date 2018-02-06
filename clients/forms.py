from django import forms
from clients.models import Client



class ClientForm(forms.ModelForm):
    """ Form for creating Client
    """
    class Meta:
        model = Client
        fields = ('display_name', 'email', 'first_name', 'last_name', 'mobile', 'middle_name', )

    def __init__(self,*args, **kwargs):
        """Client needs company for filtering
        """
        self.company = kwargs.pop('company', None)
        return super(ClientForm, self).__init__(*args, **kwargs)

    def clean_display_name(self):
        """For unique validation in display_name
        """
        display_name = self.cleaned_data['display_name']
        if not self.instance:
            display_name_q = Client.objects.filter(display_name__exact=display_name, company=self.company)
            if display_name_q:
                raise forms.ValidationError("Display name already exists:")
        if self.instance.display_name != display_name:
            if display_name_q.exists():
                raise forms.ValidationError("Display name already exists:")
        return display_name

    def clean_mobile(self):
        """For unique validation in mobile
        """
        mobile = self.cleaned_data['mobile']
        if not self.instance:
            mobile_q = Client.objects.filter(mobile__exact=mobile, company=self.company)
            if mobile_q:
                raise forms.ValidationError("Mobile already exists:")
        if self.instance.mobile != mobile:
            if mobile_q.exists():
                raise forms.ValidationError("Mobile already exists:")
        return mobile

