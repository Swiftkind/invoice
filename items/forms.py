import datetime


from django import forms
from django.conf import settings


from clients.models import Client
from items.models import Item
from invoices.models import Invoice
from datetime import  date 



class ItemForm(forms.ModelForm): 
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Item
        fields = ('item_type', 
                  'order_number', 
                  'description', 
                  'rate', 
                  'quantity', 
                  'amount', 
                  'total_amount'
                  )

    def clean_amount(self):
        """amount validation
        """
        item_type = self.data.get('item_type')
        amount = self.data.get('amount')
        if item_type == Item.FIXED:
            if not amount:
                raise forms.ValidationError("you pick fixed - amount should have a value")
        return amount

    def clean_rate(self):
        """rate validation
        """
        quantity = self.data.get('quantity')
        rate = self.data.get('rate')
        if rate:
            if not quantity:
                raise forms.ValidationError("rate has value but doest have an quantity/s")
        if not rate and quantity:
            raise forms.ValidationError("quantity has value and rate must have value too")
        return rate

    def clean_quantity(self):
        """quantity validation
        """
        item_type = self.data.get('item_type')
        quantity = self.data.get('quantity')
        rate = self.data.get('rate')
        if item_type == Item.QUANTITY:
            if not quantity:
                raise forms.ValidationError("you pick quantity - quantity must have a value")
        return quantity

    def save(self,commit=False):
        """save invoice form
        """
        instance = super(ItemForm, self).save(commit=False)
        item_type = self.data.get('item_type')
        amount = self.data.get('amount')
        quantity = self.data.get('quantity')
        rate = self.data.get('rate')

        if item_type == Item.FIXED:
            instance.amount = amount
            instance.quantity = None
            instance.rate = None
            instance.total_amount = amount
        elif item_type == Item.QUANTITY :
            instance.amount = None
            instance.quantity = quantity
            instance.rate = rate
            instance.total_amount = (int(quantity)*int(rate) )
        if commit:
            instance.save()
        return instance

