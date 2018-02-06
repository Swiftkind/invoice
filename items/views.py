import tempfile , time, os, errno


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.template.loader import get_template 
from django.views.generic import TemplateView


from clients.forms import ClientForm
from clients.models import Client
from invoices.models import Invoice
from invoices.forms import InvoiceForm, InvoiceEmailForm
from items.models import Item
from items.forms import ItemForm
from items.mixins import UserIsOwnerMixin
from users.models import User

# for pdf
from xhtml2pdf import pisa 
from io import BytesIO



class ItemListView(LoginRequiredMixin,TemplateView):
    """Display list of invoice
    """
    template_name = 'items/all_item.html'

    def get(self, *args, **kwargs):
        """Display invoices data
        """
        context = {}
        items = Item.objects.filter( company=self.request.user.company)
        query = self.request.GET.get("q")
        if query:
            items = items.filter(order_number__icontains=query)
        context['items'] =  items
        return render(self.request, self.template_name, context)



class ItemView(UserIsOwnerMixin,TemplateView):
    """View invoice information
    """
    template_name = 'items/view_item.html'

    def get(self, *args, **kwargs):
        """Get invoice information
        """
        item = get_object_or_404(Item, pk=kwargs['item_id'])
        item.save()
        context = {'item': item, }
        return render(self.request, self.template_name, context)



class ItemAddView(LoginRequiredMixin,TemplateView):
    """Adding invoice
    """
    template_name = 'items/update_item.html'

    def get(self, *args, **kwargs):
        """Display invoice form
        """
        context = {}
        context['form'] = ItemForm()
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """Get filled invoice form and create
        """
        form = ItemForm(self.request.POST)
        if  form.is_valid() :
            item = form.save(commit=False)
            item.owner = self.request.user
            item.company = self.request.user.company
            item.save()
            messages.success(self.request, 'Item is successfully Added')
            return redirect('items')
        else:
            context = {}
            context['form'] = form
            return render(self.request, self.template_name, context)



class ItemEditView(UserIsOwnerMixin,TemplateView):
    """Editing invoice
    """
    template_name = 'items/update_item.html'

    def get(self, *args, **kwargs):
        """Display invoice form
        """
        item = get_object_or_404(Item, pk=kwargs['item_id'])
        context = {}
        context['form'] = ItemForm(instance=item)
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """Get filled invoice form and create invoice
        """
        item = get_object_or_404(Item, pk=kwargs['item_id'])
        form = ItemForm(self.request.POST, instance=item)
        if  form.is_valid() :
            item = form.save(commit=False)
            item.save()
            messages.success(self.request, 'Item is successfully updated')
            return redirect('items')
        else:
            context = {}
            context['form'] = ItemForm(self.request.POST)
        return render(self.request, self.template_name, context)



class ItemDeleteView(UserIsOwnerMixin,TemplateView):
    """Delete invoice
    """
    def get(self,  *args, **kwargs):
        """Display invoice data
        """
        item = get_object_or_404(Item, pk=kwargs['item_id'])
        item.delete()
        messages.error(self.request, 'Client is successfully deleted')
        return redirect('items')


