import tempfile , time, os, errno

from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.db.models import Q
from django.forms import formset_factory
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView


from clients.forms import ClientForm
from clients.models import Client
from invoices.mixins import PdfMixin, UserIsOwnerMixin
from invoices.models import Invoice, Item
from invoices.forms import (ItemForm, 
                            ItemInlineFormSet,
                            InvoiceForm, 
                            InvoiceEmailForm, 
                    )
from users.models import User

from xhtml2pdf import pisa 
from io import BytesIO


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        """ Display invoices, clients and client add form
        """
        clients = Client.objects.filter(company=self.request.user.company)
        invoices = Invoice.objects.filter(company=self.request.user.company)
        context = {}
        context['invoices'] = Invoice.objects.filter(company=self.request.user.company)
        context['clients'] =  Client.objects.filter(company=self.request.user.company)
        context['client_form'] = ClientForm() 

        query = self.request.GET.get("q")
        if query:
            clients = clients.filter(display_name__icontains=query, owner=self.request.user)

        context['clients'] =  clients
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """Client add form
        """
        client_form = ClientForm(self.request.POST)
        if client_form.is_valid() :
            client = client_form.save(commit=False)
            client.owner = self.request.user
            client.company = self.request.user.company
            client.save()
            messages.success(self.request, 'Client is successfully added')
            return redirect('index')
        else:
            context = super().get_context_data(**kwargs)
            context['client_form'] = client_form
            context['invoices'] = Invoice.objects.filter(company=self.request.user.company)
            context['clients'] =  Client.objects.filter(company=self.request.user.company)
        return render(self.request, self.template_name, context=context)


class MakeInvoiceView(LoginRequiredMixin,TemplateView):
    """Make an invoice for client
    """
    template_name = 'invoices/add_invoice.html'

    def get(self, *args, **kwargs):
        """Displaying invoice data and invoice form
        """
        context = {}
        context['client'] = get_object_or_404(Client, pk=kwargs['client_id'])
        context['invoice_form'] = InvoiceForm()
        context['invoice_form'].fields['client'].empty_label = None
        context['invoice_form'].fields['client'].queryset =  Client.objects.filter(
                                                                            pk=kwargs['client_id']
                                                                            )
        context['invoice_form'].fields['item'].queryset =  Item.objects.filter(
                                                                company=self.request.user.company
                                                                )
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """Get filled invoice form and create invoice
        """
        invoice_form = InvoiceForm(self.request.POST)
        if  invoice_form.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.owner = self.request.user
            invoice.company = self.request.user.company
            invoice.save()
            client = Client.objects.get(pk = kwargs['client_id'])
            client.invoiced = True
            client.save()
            messages.success(self.request, 'Client is successfully invoiced')
            return redirect('index')
        else:
            context = {}
            context['invoice_form'] = invoice_form
            context['invoice_form'].fields['client'].queryset =  Client.objects.filter(
                                                                company=self.request.user.company
                                                                )
        return render(self.request, self.template_name, context)


class InvoiceView(LoginRequiredMixin ,TemplateView):
    """Display invoice
    """
    template_name = 'invoices/all_invoice.html'

    def get(self, *args, **kwargs):
        """ View invoice info and add invoice
        """
        query = self.request.GET.get("q")
        if query:
            invoices = invoices.filter(invoice_number__icontains=query
                       ).order_by('-date_updated')
        else:
            invoices = Invoice.objects.filter(company=self.request.user.company
                       ).order_by('-date_updated')

        formset = OrderInlineFormSet(queryset = Item.objects.none())

        context = {}
        context['client_form'] = ClientForm()
        context['formset'] = formset
        context['invoices'] =  invoices 
        context['invoice_form'] = InvoiceForm()
        context['invoice_form'].fields['client'].queryset =  Client.objects.filter(
                                                                company=self.request.user.company,
                                                                archive=False
                                                             ).order_by('-date_updated')
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """ Create and Add invoice
        """
        invoice_form = InvoiceForm(self.request.POST, company=self.request.user.company)
        formset = OrderInlineFormSet(self.request.POST, queryset = Item.objects.none())
        context = {}

        if  invoice_form.is_valid() and formset.is_valid():
            # Save invoice
            invoice = invoice_form.save(commit=False)
            invoice.owner = self.request.user
            invoice.company = self.request.user.company
            invoice.save()

            # Check latest item id
            try:
                latest = Item.objects.latest('id')
                item_id = latest.id + 1
            except:
                latest = 0
                item_id = latest + 1

             # Save item/s
            items = formset.save(commit=False)
            for count,item in enumerate(items):
                item.id = item_id+count
                item.owner = self.request.user
                item.invoice = invoice
                item.save()
            messages.success(self.request, 'Invoice is successfully Added')
            return redirect('invoices')
        else:
            invoices = Invoice.objects.filter(company=self.request.user.company
                       ).order_by('-date_updated')
            
            context['invoices'] =  invoices 
            context['invoice_form'] = invoice_form
            context['invoice_form'].fields['client'].queryset = Client.objects.filter(
                                                                company=self.request.user.company,
                                                                archive=False
                                                    ).order_by('-date_updated')
            context['formset'] = formset
            context['client_form'] = ClientForm(self.request.POST)
            return render(self.request, self.template_name, context)
        return render(self.request, self.template_name, context)


class UpdateInvoiceForm(UserIsOwnerMixin, TemplateView):
    """ Update form
    """
    template_name = 'invoices/all_invoice.html'

    def get(self, *args, **kwargs):
        invoices = Invoice.objects.filter(company=self.request.user.company
                   ).order_by('-date_updated')
        
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        item = ItemForm(instance=invoice)
        formset = OrderInlineFormSet(queryset = item.instance.item_set.all(), )
        
        context = {}
        context['formset'] = formset
        context['invoices'] =  invoices 
        context['invoice_form'] = InvoiceForm(instance=invoice)
        context['invoice_form'].fields['client'].queryset =  Client.objects.filter(
                                                                company=self.request.user.company,
                                                                archive=False
                                                                ).order_by('-date_updated')
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        invoice_form = InvoiceForm(self.request.POST, 
                                   company=self.request.user.company, 
                                   instance=invoice,
                        )
        item = ItemForm(instance=invoice)
        formset = OrderInlineFormSet(self.request.POST, queryset = item.instance.item_set.all())
        context = {}

        if  invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.owner = self.request.user
            invoice.company = self.request.user.company
            invoice.save()
            items = formset.save(commit=False)
            for item in items:
                item.save()
            messages.success(self.request, 'Invoice is successfully Updates')
            return redirect('invoices')
        else:
            invoices = Invoice.objects.filter(company=self.request.user.company
                                      ).order_by('-date_updated')
            context['invoices'] =  invoices 
            context['invoice_form'] = invoice_form
            context['invoice_form'].fields['client'].queryset = Client.objects.filter(
                                                                company=self.request.user.company,
                                                                archive=False
                                                                ).order_by('-date_updated')
            context['formset'] = formset
            context['client_form'] = ClientForm(self.request.POST)
            return render(self.request, self.template_name, context)
        return render(self.request, self.template_name, context=context)


class InvoiceAjaxView(UserIsOwnerMixin, View):
    """View invoice information
    """
    def get(self, *args, **kwargs):
        """Display invoice details
        """
        invoice = get_object_or_404(Invoice, id=kwargs['invoice_id'])
        invoice_number = str(invoice)
        client = str(invoice.client)
        items = Item.objects.filter(invoice=kwargs['invoice_id'])
        invoiceData = serializers.serialize('json', [invoice])
        itemsData = serializers.serialize('json', items)
        data = {
            'client': client,
            'invoice_number': invoice_number,
            'invoice': invoiceData,
            'items': itemsData,
            'prefix': invoice.client.get_prefix(),
        }
        return JsonResponse(data, safe = False, status=200)


class InvoiceDeleteView(UserIsOwnerMixin,TemplateView):
    """Delete invoice
    """
    def get(self,  *args, **kwargs):
        """Display invoice data
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        invoice.delete()
        messages.error(self.request, 'Client is successfully deleted')
        return redirect('invoices')


class PdfPreview(UserIsOwnerMixin, PdfMixin, View):
    """ Pdf preview
    """
    def get(self, *args, **kwargs):
        """Display pdf in browser
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        context = {}
        context['logo'] = f"{settings.MEDIA_ROOT}{invoice.company.logo}"
        context['invoice'] = invoice
        pdf = self.render_to_pdf_and_view('invoices/pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class InvoiceEmailView(UserIsOwnerMixin, PdfMixin, TemplateView):
    """Email an invoice
    """
    template_name = 'invoices/email.html'

    def get(self, *argrs, **kwargs):
        """Display invoice data and email form
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        email_form = InvoiceEmailForm()
        context = {}
        context['email_form'] = email_form
        context['company_email'] = invoice.owner.email
        context['send_email'] = invoice.client.email
        return render(self.request, self.template_name, context)

    def post(self, *argrs, **kwargs):
        """Save pdf and email invoice
        """
        form = InvoiceEmailForm(self.request.POST)
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        if form.is_valid():
            context = {}
            try:
                context['logo'] = str(settings.MEDIA_ROOT)+str(invoice.company.logo)
            except:
                context['logo'] = None
            context['invoice'] = invoice
            pdf = self.render_to_pdf_and_save('invoices/pdf.html', context)

            # Send email
            subject = form.cleaned_data['subject']
            text_content = form.cleaned_data['text'] 
            from_email = self.request.user.email 
            to = invoice.client.email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_file(pdf)
            msg.send()
            invoice.status = 'Sent'
            invoice.save()
            messages.success(self.request, 'Invoice is successfully sent')
            return redirect('invoices') 
        else:
            context = {}
            email_form = InvoiceEmailForm(self.request.POST)
            context['email_form'] = email_form
            context['company_email'] = invoice.owner.email
            context['send_email'] = invoice.client.email
        return render(self.request, self.template_name, context)