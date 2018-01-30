from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Q

from clients.models import *
from clients.forms import  *

from invoices.models import Invoice

from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from io import BytesIO
import time



class ClientsView(LoginRequiredMixin,TemplateView):
	template_name = 'clients/all_client.html'

	def get_context_data(self,request,**kwargs):
		#import pdb; pdb.set_trace()
		context = super().get_context_data(**kwargs)
		try :
			clients = Client.objects.filter( owner=request.user)
		except:
			clients = Client.objects.all()
		try:
			context['clients'] = Client.objects.filter(owner=request.user)
		except:
			context['clients'] = Client.objects.all()
		#context['invoices'] = Invoice.objects.filter(user_createdby=request.user.company_name, client_name=Client.objects.all())
		#context['client_fil'] = 
		query = request.GET.get("q")
		if query:
			try:
				clients = clients.filter(Q(display_name__icontains=query,  owner=request.user) )
			except:
				clients = clients.filter(Q(display_name__icontains=query) )
		context['clients'] =  clients
		return context

	def get(self, request, *args, **kwargs):
		#import pdb; pdb.set_trace()
		context = self.get_context_data(request,**kwargs)
		
		return render(self.request, self.template_name, context=context)



class ClientViewView(LoginRequiredMixin,TemplateView):
	template_name = 'clients/view_client.html'
	
	def get(self, *args, **kwargs):
		context = {
				'client': get_object_or_404(Client, id=kwargs['client_id']),
				'current_path': self.request.path,
				'invoices' : Invoice.objects.filter(client=kwargs['client_id']),
			}
		return render(self.request, self.template_name, context)



class ClientAddView(LoginRequiredMixin,TemplateView):
	template_name = 'clients/update_client.html'

	def get(self, *args, **kwargs):
		return render(self.request, self.template_name, context=self.get_context_data(**kwargs))

	def post(self, *args, **kwargs):
		#import pdb; pdb.set_trace()
		client_form = ClientForm(self.request.POST,user=self.request.user)	
		#import pdb; pdb.set_trace()
		if client_form.is_valid() :
			
			client = client_form.save(commit=False)		
			
			client.save()
			messages.success(self.request, 'Client is successfully added')
			return redirect('clients')
			
		else:
			context = {
				'client_form' : client_form,
				

				'client_form_errors' : client_form.errors,

			}
		return render(self.request, self.template_name, context=context)

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['client_form'] = ClientForm() 
		return context



class ClientEditView(LoginRequiredMixin,TemplateView):
	template_name = 'clients/update_client.html'

	def get(self, *args, **kwargs):
		return render(self.request, self.template_name, context=self.get_context_data(**kwargs))

	def post(self, request, *args, **kwargs):
		client = get_object_or_404(Client, id=kwargs['client_id'])
				
		client_form             = ClientForm(self.request.POST,instance=client)
		
		if client_form.is_valid() :
			try:
				client = client_form.save(commit=False,    owner=request.user)
			except:
				client = client_form.save(commit=False)
			client.save()
			messages.success(request, 'Client is successfully updated')
			return redirect('clients')
		else:
			context = {
				'client_form' : client_form,
				
				'client_form_errors' : client_form.errors,
				
			}
		return render(self.request, self.template_name, context=context)

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		client = get_object_or_404(Client, id=kwargs['client_id'])
		context['client_form'] = ClientForm(instance=client)
		return context

class ClientDeleteView(LoginRequiredMixin,View):
	
	def get(self, request, *args, **kwargs):
		client = get_object_or_404(Client, id=kwargs['client_id'])
		client.delete()
		messages.error(request, 'Client is successfully deleted')
		return redirect('clients')