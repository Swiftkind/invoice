from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import *
from clients.forms import  *

class ClientsView(LoginRequiredMixin,TemplateView):
	template_name = 'clients/all_client.html'

	def get(self, request, *args, **kwargs):
		return render(self.request, self.template_name, {'clients': Client.objects.all()})

class ClientViewView(LoginRequiredMixin,TemplateView):
	template_name = 'clients/view_client.html'
	def get(self, request, *args, **kwargs):
		context = {
				'client': get_object_or_404(Client, id=kwargs['client_id']),
				'current_path': self.request.path,
			}
		return render(self.request, self.template_name, context)

class ClientAddView(LoginRequiredMixin,TemplateView):
	template_name = 'clients/add_client.html'

	def get(self, request, *args, **kwargs):
		return render(self.request, self.template_name, context=self.get_context_data(**kwargs))

	def post(self, request, *args, **kwargs):
		client_form = ClientForm(self.request.POST)
		billing_address_form  = BillingAddressForm(self.request.POST, prefix='billing')
		shipping_address_form = ShippingAddressForm(self.request.POST, prefix='shipping')

		if client_form.is_valid() and billing_address_form.is_valid() and shipping_address_form.is_valid():
			client = client_form.save(commit=False)
			client.billing_address    = billing_address_form.save()
			client.shipping_address   = shipping_address_form.save()
			client.save()
			return redirect('clients')
		else:
			context = get_context_data(**kwargs)
		return render(self.request, self.template_name, context=self.get_context_data(**kwargs))

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['client_form'] = ClientForm() 
		context['billing_address_form']  = BillingAddressForm(prefix='billing')
		context['shipping_address_form'] = ShippingAddressForm(prefix='shipping')
		return context


class ClientEditView(LoginRequiredMixin,TemplateView):
	template_name = 'clients/add_client.html'

	def get(self, request, *args, **kwargs):
		return render(self.request, self.template_name, context=self.get_context_data(**kwargs))

	def post(self, request, *args, **kwargs):
		client = get_object_or_404(Client, id=kwargs['client_id'])
				
		client_form             = ClientForm(self.request.POST,instance=client)
		billing_address_form    = BillingAddressForm(self.request.POST,instance=client.billing_address, prefix='billing')
		shipping_address_form   = ShippingAddressForm(self.request.POST,instance=client.shipping_address, prefix='shipping')
		additional_address_form = AdditionalAddressForm(self.request.POST,instance=client.additional_address, prefix='additional')

		if client_form.is_valid() and billing_address_form.is_valid() and shipping_address_form.is_valid() and additional_address_form.is_valid() :
			client = client_form.save(commit=False)
			client.billing_address    = billing_address_form.save()
			client.shipping_address   = shipping_address_form.save()
			client.additional_address = additional_address_form.save() 
			client.save()
			return redirect('clients')
		else:
			context = get_context_data(**kwargs)
		return render(self.request, self.template_name, context=self.get_context_data(**kwargs))

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		client = get_object_or_404(Client, id=kwargs['client_id'])
		context['client_form'] = ClientForm(instance=client)
		context['billing_address_form']   = BillingAddressForm(instance=client.billing_address, prefix='billing')
		context['shipping_address_form']  = ShippingAddressForm(instance=client.shipping_address, prefix='shipping')
		context['additional_address_form']= AdditionalAddressForm(instance=client.additional_address, prefix='additional')
		return context

class ClientDeleteView(LoginRequiredMixin,View):
	def get(self, request, *args, **kwargs):
		client = get_object_or_404(Client, id=kwargs['client_id'])
		client.delete()
		return redirect('clients')