import datetime

from django import forms
from django.conf import settings
from django.forms import BaseFormSet, formset_factory


from clients.models import Client
from datetime import  date 
from invoices.models import Invoice, Item


class InvoiceForm(forms.ModelForm):
    """invoice form
    """
    due_date =  forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), 
                                                       input_formats=settings.DATE_INPUT_FORMATS
                                                      )
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), 
                                                          input_formats=settings.DATE_INPUT_FORMATS
                                                         )

    class Meta:
        model = Invoice
        fields = ( 'client',
                   'due_date',  
                   'invoice_number', 
                   'invoice_date',
                   'remarks',
                   'description', 
                   'payment_status',
                   'subtotal',
                   )

    def __init__(self,*args, **kwargs):
        """Invoice needs company for filtering
        """
        self.company = kwargs.pop('company', None)
        return super(InvoiceForm, self).__init__(*args, **kwargs)

    def clean_invoice_date(self):
        """ Invoice date validation
        """
        in_date = self.cleaned_data.get('invoice_date')
        in_date = datetime.datetime.strftime( in_date, '%Y-%m-%d')
        current = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        if current > in_date:
            raise forms.ValidationError("Date should be in future")
        return in_date

    def clean_due_date(self):
        """ Due date validation
        """
        due_date =  self.cleaned_data.get('due_date')
        due_date = datetime.datetime.strftime( due_date, '%Y-%m-%d')
        current = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        if current > due_date:
            raise forms.ValidationError("Date should be in future")
        return due_date

    def clean_invoice_number(self):
        """ Invoice number unique together validation 
        """
        invoice_number = self.cleaned_data.get('invoice_number')
        invoice_number_q = Invoice.objects.filter(invoice_number__exact=invoice_number, 
                                                  company=self.company
                                            )
        if not self.instance :
            if invoice_number_q.exists():
                raise forms.ValidationError("Invoice Number already exists:")
        if self.instance.invoice_number != invoice_number:
            if invoice_number_q.exists():
                raise forms.ValidationError("Invoice Number already exists:")
        return invoice_number


class InvoiceEmailForm(forms.Form):
    """invoice form for send email
    """
    subject = forms.CharField(max_length=100, required=True)
    text = forms.CharField(max_length=255, required=True)

    class Meta:
        fields = ('subject','text')

    def clean_subject(self):
        """subject validation
        """
        subject = self.cleaned_data['subject']
        if not subject:
            raise forms.ValidationError("This is required")
        return subject

    def clean_text(self):
        """text validation
        """
        text = self.cleaned_data['text']
        if not text:
            raise forms.ValidationError("This is required")
        return text


class ItemForm(forms.ModelForm):
    """ Add item form 
    """
    class Meta:
        model = Item
        fields = ('description',
                  'quantity',
                  'rate'
                )


class BaseItemFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        for count,form in enumerate(self.forms):
            if not form.data['form-'+str(count)+'-description']:
                raise forms.ValidationError("Description is required!")
            if not form.data['form-'+str(count)+'-quantity']:
                raise forms.ValidationError("Quantity is required!")
            if not form.data['form-'+str(count)+'-rate']:
                raise forms.ValidationError("Rate is required!")
