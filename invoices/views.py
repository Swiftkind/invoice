from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template 


from invoices.mixins import PdfMixin
from invoices.models import Invoice
from invoices.forms import InvoiceForm, InvoiceEmailForm
from invoices.mixins import PdfMixin
from clients.forms import ClientForm
from clients.models import Client
from users.models import User


from invoices.utils import render_to_pdf
from xhtml2pdf import pisa 
from io import BytesIO
import tempfile , time, os, errno



class IndexView(LoginRequiredMixin,TemplateView):
    """Displaying dashboard index
    """
    template_name = 'index.html'


    def get_context_data(self,**kwargs):
        """Get the data of clients and invoices 
        """
        context = super().get_context_data(**kwargs)
        clients = Client.objects.filter( company=self.request.user.company)
        context['invoices'] = Invoice.objects.filter( company=self.request.user.company)
        context['client_form'] = ClientForm() 
        query = self.request.GET.get("q")
        if query:
            clients = clients.filter(Q(display_name__icontains=query,  company=self.request.user.company))
        context['clients'] =  clients
        return context


    def get(self, *args, **kwargs):
        """Gisplaying clients and invoices
        """
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context=context)


    def post(self, *args, **kwargs):
        """Get the filled client form and create client
        """
        client_form = ClientForm(self.request.POST,user=self.request.user)
        if client_form.is_valid() :
            client = client_form.save(commit=False)
            client.save()
            messages.success(self.request, 'Client is successfully added')
            return redirect('index')
        else:
            context = super().get_context_data(**kwargs)
            context['client_form'] = client_form
            context['client_form_errors' ] = client_form.errors
            context['invoices'] = Invoice.objects.filter( company=self.request.user.company)
            context['clients'] =  Client.objects.filter(  company=self.request.user.company)
        return render(self.request, self.template_name, context=context)



class MakeInvoiceView(LoginRequiredMixin,TemplateView):
    """Make an invoice for client
    """
    template_name = 'invoices/update_invoice.html'


    def get_context_data(self,**kwargs):
        """Get client data, invoice data and invoice form
        """
        context = super().get_context_data(**kwargs)
        context['client'] = get_object_or_404(Client, pk=kwargs['client_id'])
        context['invoice_form'] = InvoiceForm()
        context['invoice_form'].fields['client'].empty_label = None
        context['invoice_form'].fields['client'].queryset =  Client.objects.filter(pk=kwargs['client_id'])
        context['invoice'] = int(str(Invoice.objects.latest('pk'))) + 1
        return context


    def get(self, *args, **kwargs):
        """Displaying invoice data and invoice form
        """
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)


    def post(self, *args, **kwargs):
        """Get filled invoice form and create invoice
        """
        invoice_form = InvoiceForm(self.request.POST, user=self.request.user)
        if  invoice_form.is_valid() :       
            invoice = invoice_form.save(commit=False) 
            invoice.save()
            client = Client.objects.get(pk = kwargs['client_id'])
            client.invoiced = True
            client.save()
            messages.success(self.request, 'Client is successfully invoiced')
            return redirect('index')
        else:
            context =self.get_context_data(**kwargs)
            context['invoice_form'] = invoice_form
            context['invoice_form'].fields['client'].queryset =  Client.objects.filter(company=self.request.user.company)
            context['invoice'] = int(str(Invoice.objects.latest('pk'))) + 1
        return render(self.request, self.template_name, context)



class InvoiceListView(LoginRequiredMixin,TemplateView):
    """Display list of invoice
    """
    template_name = 'invoices/all_invoice.html'


    def get_context_data(self,**kwargs):
        """Get invoices data
        """
        context = super().get_context_data(**kwargs)
        invoices = Invoice.objects.filter( company=self.request.user.company)
        query = self.request.GET.get("q")
        if query:
            invoices = invoices.filter(Q(invoice_number__icontains=query,  company=self.request.user.company) )
        context['invoices'] =  invoices
        return context


    def get(self, *args, **kwargs):
        """Display invoices data
        """
        context = self.get_context_data(**kwargs) 
        return render(self.request, self.template_name, context)



class InvoiceView(LoginRequiredMixin,PdfMixin,TemplateView):
    """View invoice information
    """
    template_name = 'invoices/view_invoice.html'


    def get(self, *args, **kwargs):
        """Get invoice information
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        self.save_pdf(**kwargs)
        invoice.pdf = str(self.get_invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
        invoice.save()
        context = { 'invoice': invoice,
                    'pdf' : invoice.pdf,
                    }
        return render(self.request, self.template_name, context)



class InvoiceAddView(LoginRequiredMixin,TemplateView):
    """Adding invoice
    """
    template_name = 'invoices/update_invoice.html'


    def get_context_data(self,**kwargs):
        """Get invoice form
        """
        context = super().get_context_data(**kwargs)
        context['invoice_form'] = InvoiceForm()
        context['invoice_form'].fields['client'].queryset =  Client.objects.filter( company=self.request.user.company)
        context['invoice'] = int(str(Invoice.objects.latest('pk'))) + 1
        return context


    def get(self, *args, **kwargs):
        """Display invoice form
        """
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)


    def post(self, *args, **kwargs):
        """Get filled invoice form and create
        """
        invoice_type = self.request.POST['invoice_type']
        invoice_form = InvoiceForm(self.request.POST, user=self.request.user, invoice_type=invoice_type )
        if  invoice_form.is_valid() :
            invoice = invoice_form.save(commit=False,company=self.request.user.company)
            invoice.save()
            messages.success(self.request, 'Invoice is successfully Added')
            return redirect('invoices')
        else:
            context =self.get_context_data(**kwargs)
            context['invoice_form'] = invoice_form
            context['invoice_form'].fields['client'].queryset =  Client.objects.filter( company=self.request.user.company)
            context['invoice'] = int(str(Invoice.objects.latest('pk'))) + 1      
        return render(self.request, self.template_name, context)



class InvoiceEditView(LoginRequiredMixin,TemplateView):
    """Editing invoice
    """
    template_name = 'invoices/update_invoice.html'


    def get_context_data(self,**kwargs):
        """Get invoice form fields
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        context = super().get_context_data(**kwargs)
        context['invoice_form'] = InvoiceForm(instance=invoice)
        context['invoice_form'].fields['client'].queryset =  Client.objects.filter( owner=self.request.user)
        context['invoice'] = int(str(Invoice.objects.latest('pk'))) 
        return context


    def get(self, *args, **kwargs):
        """Display invoice form
        """
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)


    def post(self, *args, **kwargs):
        """Get filled invoice form and create invoice
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        invoice_form = InvoiceForm(self.request.POST, instance=invoice, user=self.request.user)
        if  invoice_form.is_valid() :
            invoice = invoice_form.save(commit=False)
            invoice.save()
            messages.success(self.request, 'Invoice is successfully updated')
            return redirect('invoices')
        else:
            context = self.get_context_data(**kwargs)
            context['invoice_form'] = InvoiceForm(self.request.POST)
        return render(self.request, self.template_name, context)



class InvoiceDeleteView(LoginRequiredMixin,TemplateView):
    """Delete invoice
    """
    def get(self,  *args, **kwargs):
        """Display invoice data
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        invoice.delete()
        messages.error(self.request, 'Client is successfully deleted')
        return redirect('invoices')



class InvoiceEmailView(LoginRequiredMixin,PdfMixin, TemplateView):
    """Email an invoice
    """
    template_name = 'invoices/email.html'


    def get_context_data(self,**kwargs):
        """Get invoice data and email form
        """
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        email_form = InvoiceEmailForm()

        context = super().get_context_data(**kwargs)
        context['email_form'] = email_form
        context['company_email'] = invoice.owner.email
        context['send_email'] = invoice.client.email
        self.save_pdf(**kwargs)
        invoice.pdf = str(self.get_invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
        invoice.save()
        context['pdf'] = invoice.pdf
        return context


    def get(self, *argrs, **kwargs):
        """Display invoice data and email form
        """
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)


    def post(self, *argrs, **kwargs):
        """Save pdf and email invoice
        """
        form = InvoiceEmailForm(self.request.POST)
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        if form.is_valid():
            self.save_pdf(**kwargs)
            invoice.pdf = str(self.get_invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
            invoice.save()
            pdf = settings.MEDIA_ROOT+str(invoice.pdf)

            """Html Template for viewing in email
            """
            head = '<!DOCTYPE html><html><head><title>Invoice</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'
            style1 =  '<style>div#header {background-color: #1a382a;}div h1#header-text {text-align: center;color: #7bc1b8;}h3 {text-align: center;}'
            style2 =  'h2 {text-align: center;color: #d22f2f;}div#middle {background-color: #f2f5f2;border: 1px solid #b1c5b4;}p.content{margin-left: 40%}</style></head>'
            body1 = '<body><div class="col-md-12" id="header"><h1 id="header-text">Invoice Number</h1></div><div class="col-md-12"><div class="col-md-3" id="left"></div>'
            body2 = '<div class="col-md-6"><div class="col-md-12"><br><p>Dear mi kill,</p><br><p>Thank you for your business. Your invoice can be viewed, printed and downloaded as PDF from the link below. You can also choose to pay it online. </p>'
            body3 = '<br></div><div class="col-md-12" id="middle"><div class="col-md-12"><h3>INVOICE AMOUNT</h3><h2><strong>PHP 5.00 </strong></h2><hr></div><div class="col-md-12"  >'
            body4 = '<div class="col-md-12"><div class="col-md-6"><p class="content">Invoice No.</p></div><div class="col-md-6"><p class="content">345</p></div></div>'
            body5 = '<div class="col-md-12"><div class="col-md-6"><p class="content">Invoice Date</p></div><div class="col-md-6"><p class="content">jan 45</p></div></div>'
            body6 = '<div class="col-md-12"><div class="col-md-6"><p class="content">Due Date</p></div><div class="col-md-6"><p class="content">jan 65</p></div></div>'
            body7 = '</div></div><div class="col-md-12"><br>Regards,<br>Michael sy<br>swiftkind</div></div><div class="col-md-3" id="right"></div></div>'

            html = head+style1+style2+body1+body2+body3+body4+body5+body6+body7

            subject, from_email, to = form.cleaned_data['subject'],'michaelpsy71095@gmail.com','firstlastzoh0@gmail.com'
            text_content = form.cleaned_data['text']
            html_content = html
            
            """Send invoice email
            """
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.attach_file(pdf)
            msg.send()
            messages.success(self.request, 'Invoice is successfully sent')
            return redirect('invoices') 
        else:
            context = super().get_context_data(**kwargs)
            email_form = InvoiceEmailForm()
            context['email_form'] = email_form
            context['email_form_errors' ] = email_form.errors
            self.save_pdf(**kwargs)
            invoice.pdf = str(self.get_invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
            invoice.save()
            context['company_email'] = invoice.owner.email
            context['send_email'] = invoice.client.email
            context['pdf'] = invoice.pdf
        return render(self.request, self.template_name, context)



class GeneratePdf(TemplateView):
    """Generate a pdf
    """
    def get_context_data(self,**kwargs):
        """Get data for generating pdf
        """
        user = get_object_or_404(User, pk=kwargs['user_id'])
        context = super().get_context_data(**kwargs)
        context['logo'] = str(settings.MEDIA_ROOT)+str(user.logo)
        return context


    def get(self, request, *args, **kwargs):
        """Display pdf in browser
        """
        context = self.get_context_data(**kwargs)
        pdf = render_to_pdf('invoices/pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')



class InvoicePdfView(LoginRequiredMixin,PdfMixin, TemplateView):
    """Invoice pdf view 
    """
    def get(self, *args, **kwargs):
        """Display pdf
        """
        template = get_template( settings.BASE_DIR+'/templates/invoices/pdf.html') 
        context = {'pagesize':'A4'} 
        html = template.render(context) 
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
 
