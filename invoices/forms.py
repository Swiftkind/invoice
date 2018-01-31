from django import forms
from django.conf import settings


from invoices.models import Invoice
from clients.models import Client

from datetime import datetime, date 



class InvoiceForm(forms.ModelForm):
    '''invoice form
    '''
    due_date =  forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    invoice_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS) 
    start_time = forms.TimeField(input_formats=settings.TIME_INPUT_FORMATS, required=False)
    end_time = forms.TimeField(input_formats=settings.TIME_INPUT_FORMATS, required=False)



    class Meta:
        model = Invoice
        fields = ('amount', 'client', 'due_date', 'end_time', 'hours', 'invoice_number', 'invoice_type', 'invoice_date',
                  'order_number', 'paid', 'rate', 'remarks', 'start_time')


    def __init__(self,*args, **kwargs):
        """need owner by user
        need invoice type from view because cleaned_data.get('invoice_type') doesnt work in clean_hours
        """
        self.user = kwargs.pop('user', None)
        self.inv = kwargs.pop('invoice_type', None) 
        return super(InvoiceForm, self).__init__(*args, **kwargs)


    def clean_amount(self):
        """amount validation
        """
        invoice_type = self.cleaned_data.get('invoice_type')
        amount = self.cleaned_data.get('amount')
        if invoice_type == 'fixed':
            if not amount:
                raise ValidationError("you pick fixed - amount should have a value")
        return amount


    def clean_rate(self):
        """rate validation
        """
        hours = self.cleaned_data.get('hours')
        rate = self.cleaned_data.get('rate')
        if rate:
            if not hours:
                raise ValidationError("rate has value but doest have an hour/s")
        if not rate and hours:
            raise ValidationError("hours has value and rate must have value too")
        return rate


    def clean_order_number(self):
        """order number validation from unique_together
        """
        or_no = self.cleaned_data.get('order_number')
        if or_no:
            text_or_no = Invoice.objects.filter(order_number__exact=or_no)
            if text_or_no:
                raise ValidationError("Order Number already exists:")
        return or_no


    def clean_invoice_number(self):
        """invoice number valiudation from unique_together
        """
        inv_no = self.cleaned_data.get('invoice_number')
        if inv_no:
            test_inv_no = Invoice.objects.filter(invoice_number__exact=inv_no)
            if test_inv_no:
                raise ValidationError("Invoice Number already exists:")                     
        return inv_no   


    def clean_invoice_date(self):
        """invoice date validation
        """
        in_date = self.cleaned_data.get('invoice_date')
        if in_date:
            in_date = datetime.datetime.strftime( in_date, '%Y-%m-%d')
            current = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
            if current > in_date:
                raise ValidationError("Datetime should be in future")
        return in_date


    def clean_due_date(self):
        """due date validation
        """
        due_date =  self.cleaned_data.get('due_date')
        if due_date:
            due_date = datetime.datetime.strftime( due_date, '%Y-%m-%d')
            current = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
            if current > due_date:
                raise ValidationError("Datetime should be in future")
        return due_date


    def clean_hours(self):
        """hours validation
        """
        invoice_type = self.inv
        hours = self.cleaned_data.get('hours')
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        rate = self.cleaned_data.get('rate')

        """invoice type condition
        """
        if invoice_type == 'fixed':
            start_time = self.cleaned_data.get('start_time')
            end_time = self.cleaned_data.get('end_time')
        if invoice_type == 'hourly':
            start_time = self.data['start_time']
            end_time = self.data['end_time']
        
        if invoice_type == 'hourly':
            if hours:
                if start_time == '' or end_time == '':  
                    pass
                else:
                    start_time = parse(start_time).time()
                    end_time = parse(end_time).time()
                if start_time and end_time:
                    time_interval = datetime.datetime.combine(date.today(),end_time) - datetime.datetime.combine(date.today(),start_time)
                    time_interval = int(time_interval.seconds/3600)
                    if str(time_interval) != str(hours):
                        raise ValidationError("hours should equal to the time interval between start_time and end_time")
            if not hours:
                raise ValidationError("you pick hourly - hours must have a value")
        return hours



    def save(self, commit=True):
        """save invoice form
        """
        instance = super(InvoiceForm, self).save(commit=False)
        invoice_type = self.cleaned_data.get('invoice_type')
        amount = self.cleaned_data.get('amount')
        hours = self.cleaned_data.get('hours')
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        rate = self.cleaned_data.get('rate')

        """invoice type conditional
        """
        if invoice_type == 'fixed':
            instance.amount = amount
            instance.hours = None
            instance.start_time = None
            instance.end_time = None
            instance.rate = None
            instance.total_amount = amount- instance.paid
        elif invoice_type == 'hourly' :
            instance.amount = None
            instance.hours = hours
            instance.rate = rate
            instance.start_time = start_time
            instance.end_time = end_time
            instance.total_amount = (hours*rate)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance



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
            raise ValidationError("This is required")
        return subject


    def clean_text(self):
        """text validation
        """
        text = self.cleaned_data['text']
        if not text:
            raise ValidationError("This is required")
        return text


