from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string, get_template
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template 
from django.template import Context 

from invoices.mixins import PdfMixin
from invoices.models import Invoice
from invoices.forms import InvoiceForm, InvoiceEmailForm
from invoices.render import Render
from invoices.mixins import PdfMixin

from clients.forms import ClientForm
from clients.models import Client
from users.models import User

from xhtml2pdf import pisa 

from io import BytesIO
import tempfile , time, os, errno



class IndexView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		try :
			clients = Client.objects.filter( owner=self.request.user)
		except:
			clients = Client.objects.all()
		try:
			context['invoices'] = Invoice.objects.filter( owner=self.request.user)
		except:
			context['invoices'] = Invoice.objects.all()

		context['client_form'] = ClientForm() 
		query = self.request.GET.get("q")
		if query:
			try:
				clients = clients.filter(Q(display_name__icontains=query,  owner=self.request.user) )
			except:
				clients = clients.filter(Q(display_name__icontains=query) )
		context['clients'] =  clients
		return context


	def get(self, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(self.request, self.template_name,context=context)

	def post(self, *args, **kwargs):
		client_form = ClientForm(self.request.POST,user=self.request.user)
		if client_form.is_valid() :
			try:
				client = client_form.save(commit=False)
			except:
				client = client_form.save(commit=False)
			client.save()
			messages.success(self.request, 'Client is successfully added')
			return redirect('index')
		else:
			context = super().get_context_data(**kwargs)
			context['client_form'] = client_form
			context['client_form_errors' ] = client_form.errors
			try:
				context['invoices'] = Invoice.objects.filter( owner=self.request.user)
				context['clients'] =  Client.objects.filter(  owner=self.request.user)
			except:
				context['invoices'] = Invoice.objects.all()
				context['clients'] =  Client.objects.all()	
		return render(self.request, self.template_name, context=context)


class MakeInvoiceView(LoginRequiredMixin,TemplateView):
	template_name = 'invoices/update_invoice.html'


	def get_context_data(self,**kwargs):
		#import pdb; pdb.set_trace()
		context = super().get_context_data(**kwargs)
		context['client'] = get_object_or_404(Client, pk=kwargs['client_id'])
		context['invoice_form'] = InvoiceForm()
		context['invoice_form'].fields['client'].empty_label = None
		context['invoice_form'].fields['client'].queryset =  Client.objects.filter(pk=kwargs['client_id'])
		try:
			context['invoice'] = int(str(Invoice.objects.latest('pk'))) + 1
		except:
			context['invoice'] = 1
		return context

	def get(self, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(self.request, self.template_name, context)

	def post(self, *args, **kwargs):
		#import pdb; pdb.set_trace()
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
			try:
				context['invoice_form'].fields['client'].queryset =  Client.objects.filter(owner=self.request.user)
				context['invoice'] = int(str(Invoice.objects.latest('pk'))) + 1
			except:
				context['invoice_form'].fields['client'].queryset =  Client.objects.all()
				context['invoice'] = 1
		return render(self.request, self.template_name, context)



class InvoicesView(LoginRequiredMixin,TemplateView):
	template_name = 'invoices/all_invoice.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		try:
			invoices = Invoice.objects.filter( owner=self.request.user)
		except:
			invoices = Invoice.objects.all()
		try:
			context['invoices'] = Invoice.objects.filter( owner=self.request.user)
		except:
			context['invoices'] = Invoice.objects.all()
		query = self.request.GET.get("q")
		if query:
			try:
				invoices = invoices.filter(Q(invoice_number__icontains=query,  owner=self.request.user) )
			except:
				invoices = invoices.filter(Q(invoice_number__icontains=query) )
		context['invoices'] =  invoices
		return context


	def get(self, *args, **kwargs):
		context = self.get_context_data(**kwargs) 
		return render(self.request, self.template_name, context)



class InvoiceViewView(LoginRequiredMixin,PdfMixin,TemplateView):
	template_name = 'invoices/view_invoice.html'

	def get(self, *args, **kwargs):
		invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
		self.save_pdf(**kwargs)
		invoice.pdf = str(self.get_invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
		invoice.save()
		context = {
					'invoice': invoice,
					'pdf' : invoice.pdf,
					}

		return render(self.request, self.template_name, context)



class InvoiceAddView(LoginRequiredMixin,TemplateView):
	template_name = 'invoices/update_invoice.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['invoice_form'] = InvoiceForm()
		try:
			context['invoice_form'].fields['client'].queryset =  Client.objects.filter( owner=self.request.user)
			context['invoice'] = int(str(Invoice.objects.latest('pk'))) + 1
		except:
			#context['invoice_form'].fields['client'] = '' 
			context['invoice'] =  1
		return context


	def get(self, *args, **kwargs):
		#import pdb; pdb.set_trace()
		context = self.get_context_data(**kwargs)
		return render(self.request, self.template_name, context)


	def post(self, *args, **kwargs):
		#import pdb; pdb.set_trace()
		invoice_type = self.request.POST['invoice_type']
		invoice_form = InvoiceForm(self.request.POST,user=self.request.user,invoice_type=invoice_type )
		if  invoice_form.is_valid() :
			invoice = invoice_form.save(commit=False)
			invoice.save()
			messages.success(self.request, 'Invoice is successfully Added')
			return redirect('invoices')
		else:
			context =self.get_context_data(**kwargs)
			context['invoice_form'] = invoice_form
			try:
				context['invoice_form'].fields['client'].queryset =  Client.objects.filter( owner=self.request.user)
				context['invoice'] = int(str(Invoice.objects.latest('pk'))) + 1
			except:
				context['invoice_form'].fields['client'].queryset =  Client.objects.all()
				context['invoice'] =  1			
		return render(self.request, self.template_name, context)



class InvoiceEditView(LoginRequiredMixin,TemplateView):
	template_name = 'invoices/update_invoice.html'

	def get_context_data(self,**kwargs):
		invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
		context = super().get_context_data(**kwargs)
		context['invoice_form'] = InvoiceForm(instance=invoice)
		try:
			context['invoice_form'].fields['client'].queryset =  Client.objects.filter( owner=self.request.user)
			context['invoice'] = int(str(Invoice.objects.latest('pk'))) 
		except:
			context['invoice_form'].fields['client'].queryset =  Client.objects.all()
		
		return context


	def get(self, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(self.request, self.template_name, context)

	def post(self, *args, **kwargs):
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

	def get(self,  *args, **kwargs):
		invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
		invoice.delete()
		messages.error(self.request, 'Client is successfully deleted')
		return redirect('invoices')


class InvoiceEmailView(LoginRequiredMixin,PdfMixin, TemplateView):
	template_name = 'invoices/email.html'

	def get_context_data(self,**kwargs):
		#import pdb; pdb.set_trace()
		invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
		context = super().get_context_data(**kwargs)
		email_form = InvoiceEmailForm()
		context['email_form'] = email_form
		context['company_email'] = invoice.owner.email
		context['send_email'] = invoice.client.email
		self.save_pdf(**kwargs)
		invoice.pdf = str(self.get_invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
		invoice.save()
		context['pdf'] = invoice.pdf
		return context

	def get(self, *argrs, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(self.request, self.template_name, context)

	def post(self, *argrs, **kwargs):
		#import pdb; pdb.set_trace()
		form = InvoiceEmailForm(self.request.POST)
		invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
		if form.is_valid():
			self.save_pdf(**kwargs)
			invoice.pdf = str(self.get_invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
			invoice.save()
			pdf = settings.MEDIA_ROOT+str(invoice.pdf)
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
		
	

class PDF(TemplateView):
	template_name = 'invoices/pdf.html'

	def get(self,*args,**kwargs):
		return render(self.request, self.template_name)



#from easy_pdf.views import PDFTemplateView
'''
class InvoicePdfView(PDFTemplateView):
	template_name = 'invoices/pdf.html'

	base_url = 'file://' + settings.STATIC_ROOT
	download_filename = 'hello.pdf'

	def get_context_data(self, **kwargs):
		return super(InvoicePdfView, self).get_context_data(
			pagesize='A4',
			title='Hi there!',
			**kwargs
		)

	def get(self, request, *args, **kwargs):

		context = self.get_context_data(**kwargs)
		context['u'] = str(self.request.user.logo) 
		return self.render_to_response(context)

'''


from django.http import HttpResponse
from django.views.generic import View
from invoices.utils import render_to_pdf #created in step 4

class GeneratePdf(TemplateView):

	def get_context_data(self,**kwargs):
		user = get_object_or_404(User, pk=kwargs['user_id'])
		context = super().get_context_data(**kwargs)
		
		context['logo'] = str(settings.MEDIA_ROOT)+str(user.logo)
		#context['invoice'] = 
		
		return context


	def get(self, request, *args, **kwargs):
		
		context = self.get_context_data(**kwargs)
	
		pdf = render_to_pdf('invoices/pdf.html', context)
		return HttpResponse(pdf, content_type='application/pdf')


class InvoicePdfView(LoginRequiredMixin,PdfMixin, TemplateView):
	def get(self, *args, **kwargs):
		template = get_template( settings.BASE_DIR+'/templates/invoices/pdf.html') 
		context = {'pagesize':'A4'} 
		html = template.render(context) 
		response = BytesIO()
		pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
		if not pdf.err:
			return HttpResponse(response.getvalue(), content_type='application/pdf')
		else:
			return HttpResponse("Error Rendering PDF", status=400)
 

#	filename = 'my_pdf.pdf'
#	template_name = settings.BASE_DIR+'/templates/invoices/pdf.html'
#	cmd_options = {
#		'margin-top': 3,
#	}


	'''
	def g_pdf(self):
		html_string = render_to_string('invoices/update_invoice.html')
		html = HTML(string=html_string)
		result = html.write_pdf()

    # Creating http response
		response = HttpResponse(content_type='application/pdf;')
		response['Content-Disposition'] = 'inline; filename=list_people.pdf'
		response['Content-Transfer-Encoding'] = 'binary'
		with tempfile.NamedTemporaryFile(delete=True) as output:
			output.write(result)
			output.flush()
			output = open(output.name, encoding="utf-8")
			response.write(output.read()) 

		return response


	def pdf(self):
		pdf = self.g_pdf()
		return pdf
	'''

#	def get(self, *args, **kwargs):
#		user = get_object_or_404(User, pk=kwargs['user_id'])
		#user = get_object_or_404(User, pk=kwargs['user_id'])
#		print(str(settings.MEDIA_ROOT)+str(user.logo) )
		#invoice_form = InvoiceForm()
		#html_template = get_template(settings.BASE_DIR+'/templates/invoices/update_invoice.html')
		#print(html_string)

#		buff = BytesIO()
		#tmp = StringIO()
#		font_config = FontConfiguration()
		#html = HTML(string='<h1>The title</h1>')
		#css = CSS(string='''
		#		@font-face {
		#		font-family: 'Open Sans';
		#		src: url('https://fonts.googleapis.com/css?family=Open Sans');
		#		}
		#		h1 { font-family: 'Open Sans' }''', font_config=font_config)
		#html.write_pdf('/tmp/example.pdf', stylesheets=[stylesheet],font_config=font_config)


		#with open(str(settings.MEDIA_ROOT)+str(user.logo)) as image_file:
#		context = {'logo': str(settings.MEDIA_ROOT)+str(user.logo)}

#		print(user.logo.path)
#		html = settings.BASE_DIR+'/templates/invoices/pdf.html'
#		print(html)
		#response = HttpResponse(content_type='application/pdf')
		#	response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
#		return Render.render(html, context)

#		html_string = render_to_string(settings.BASE_DIR+'/templates/invoices/pdf.html', context)
#		html = HTML(string=html_string)
			#t=get_template('invoices/pdf.html')
			#html = HTML(settings.BASE_DIR+'/templates/invoices/pdf.html', {'logo': user.logo})
	#		css = CSS(settings.BASE_DIR+'/assets/css/pdf.css')
			#html = HTML(t)
			#css = CSS(string='''
			#		@page { size: A3; margin: 1cm }
			#		@font-face {
			#		font-family: 'Open Sans';
			#		src: url('https://fonts.googleapis.com/css?family=Open Sans');
			#		}
			#		h1 { font-family: 'Open Sans'; font-color:red; }''', font_config=font_config);

	#		html.write_pdf()
	#		response = HttpResponse(html,content_type='application/pdf')
			#html.write_pdf(target=settings.MEDIA_ROOT+'pdfs/mypdf.pdf', stylesheets=[css])
			#fqs = FileSystemStorage(settings.MEDIA_ROOT+'pdfs')
			#with fs.open('mypdf.pdf') as pdf:
			#	response = HttpResponse(pdf, content_type='application/pdf')
	#		response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
			#	return response
			#return response

			#html_string = render_to_string('invoices/update_invoice.html')
			#html = HTML(string=html_string)
			#result = html.write_pdf()

	    # Creating http response
		#response = HttpResponse(result,content_type='application/pdf;')
		#response['Content-Disposition'] = 'inline; filename=list_people.pdf'
		#response['Content-Transfer-Encoding'] = 'binary'
		#with tempfile.NamedTemporaryFile(delete=True) as output:
		#	output.write(result)
		#	output.flush()
		#	output = open(output.name, 'r')
		#	response.write(output.read()) 
		#return Render.render(settings.BASE_DIR+'/templates/invoices/pdf.html', context)
		#return response

#		return HttpResponse(response,content_type='application/pdf')


	
