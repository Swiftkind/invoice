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
from invoices.forms import InvoiceForm, InvoiceEmailForm, ItemForm
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


class InvoiceListView(LoginRequiredMixin ,TemplateView):
    """Display list of invoice
    """
    template_name = 'invoices/all_invoice.html'

    def get(self, *args, **kwargs):
        """Display invoices data
        """
        context = {}
        invoices = Invoice.objects.filter(company=self.request.user.company)
        query = self.request.GET.get("q")
        if query:
            invoices = invoices.filter(invoice_number__icontains=query)
        context['invoices'] =  invoices 
        context['invoice_form'] = InvoiceForm()
        context['client_form'] = ClientForm() 
        context['invoice_form'].fields['client'].queryset =  Client.objects.filter(
                                                                company=self.request.user.company
                                                                )
        ItemFormSet = formset_factory(ItemForm)
        context['formset'] = ItemFormSet()
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """Get filled invoice form and create
        """
        ItemFormSet = formset_factory(ItemForm)
        formset = ItemFormSet(self.request.POST)
        client_form = ClientForm(self.request.POST) 
        invoice_form = InvoiceForm(self.request.POST)
        
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.owner = self.request.user
            client.company = self.request.user.company
            client.save()
            messages.success(self.request, 'Client is successfully added')
            return redirect('invoices')

        if  invoice_form.is_valid() and formset.is_valid():
            # Save invoice
            invoice = invoice_form.save(commit=False)
            invoice.owner = self.request.user
            invoice.company = self.request.user.company
            invoice.save()

            try:
                latest = Item.objects.latest('id')
                item_id = latest.id + 1
            except:
                latest = 0
                item_id = latest + 1
            # Save item/s
            for count,form in enumerate(formset):
                item_form = ItemForm()
                item_id = item_id + count
                item = item_form.save(commit=False)
                item.id = item_id
                item.invoice = invoice
                item.owner = self.request.user
                item.description = form.data['form-'+str(count)+'-description']
                item.quantity = form.data['form-'+str(count)+'-quantity']
                item.rate = form.data['form-'+str(count)+'-rate']
                item.amount =  form.data['form-'+str(count)+'-amount']
                item.save()
            messages.success(self.request, 'Invoice is successfully Added')
            return redirect('invoices')
        else:
            
            invoices = Invoice.objects.filter(company=self.request.user.company)
            context = {}
            context['invoices'] =  invoices 
            context['invoice_form'] = invoice_form
            context['invoice_form'].fields['client'].queryset = Client.objects.filter(
                                                                company=self.request.user.company
                                                                )
            ItemFormSet = formset_factory(ItemForm)
            context['formset'] = ItemFormSet(self.request.POST)
 
            return render(self.request, self.template_name, context)


class InvoiceView(UserIsOwnerMixin, TemplateView):
    """View invoice information
    """
    template_name = 'invoices/view_invoice.html'

    def get(self, *args, **kwargs):
        """Display pdf in browser
        """
        invoice = get_object_or_404(Invoice, id=kwargs['invoice_id'])
        context = super().get_context_data(**kwargs)
        context['logo'] =  f"{settings.MEDIA_ROOT}{invoice.company.logo}"
        context['invoice'] = invoice
        return render(self.request, self.template_name, context)


class InvoiceAjaxView(UserIsOwnerMixin, View):
    """View invoice information
    """

    def get(self, *args, **kwargs):
        """Display pdf in browser
        """
        invoice = get_object_or_404(Invoice, id=kwargs['invoice_id'])
        data = serializers.serialize('json', [invoice])
        return JsonResponse({'invoice': data,
                            },
                              safe = False,
                              status=200
                            )


class InvoiceAddView(LoginRequiredMixin,TemplateView):
    """Adding invoice
    """
    template_name = 'invoices/update_invoice.html'

    def get(self, *args, **kwargs):
        """Display invoice form
        """
        context = {}
        context['invoice_form'] = InvoiceForm()
        context['invoice_form'].fields['client'].queryset =  Client.objects.filter(
                                                                company=self.request.user.company
                                                                )
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """Get filled invoice form and create
        """
        invoice_form = InvoiceForm(self.request.POST, company=self.request.user.company)
        if  invoice_form.is_valid() :
            invoice = invoice_form.save(commit=False)
            invoice.owner = self.request.user
            invoice.company = self.request.user.company
            invoice.save()
            messages.success(self.request, 'Invoice is successfully Added')
            return redirect('invoices')
        else:
            context = {}
            context['invoice_form'] = invoice_form
            context['invoice_form'].fields['client'].queryset = Client.objects.filter(
                                                                company=self.request.user.company
                                                                )
        return render(self.request, self.template_name, context)



class InvoiceEditView(UserIsOwnerMixin,TemplateView):
    """Editing invoice
    """
    template_name = 'invoices/update_invoice.html'

    def get(self, *args, **kwargs):
        """Display invoice form
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        context = {}
        context['invoice_form'] = InvoiceForm(instance=invoice)
        context['invoice_form'].fields['client'].queryset = Client.objects.filter(
                                                                company=self.request.user.company
                                                                )
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """Get filled invoice form and create invoice
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        invoice_form = InvoiceForm(self.request.POST, 
                                   instance=invoice, 
                                   company=self.request.user.company
                                  )
        if  invoice_form.is_valid() :
            invoice_form.save()
            messages.success(self.request, 'Invoice is successfully updated')
            return redirect('invoices')
        else:
            context = {}
            context['invoice_form'] = InvoiceForm(self.request.POST)
            context['invoice_form'].fields['client'].queryset = Client.objects.filter(
                                                                company=self.request.user.company
                                                                )
        return render(self.request, self.template_name, context)



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





