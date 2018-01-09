from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from invoice.models import Invoice
from invoice.forms import CustomerForm, PaymentForm, ItemDetailForm
# Create your views here.

class InvoiceView(TemplateView):
	template_name = 'invoice/all_invoice.html'

	def get(self, request, *args, **kwargs):
		return render(self.request, self.template_name, {'invoices': Invoice.objects.all()})

class InvoiceViewView(TemplateView):
	template_name = 'invoice/view_invoice.html'

	def get(self, request, *args, **kwargs):
		invoice = get_object_or_404(Invoice, id=kwargs['invoice_id'])
		return render(self.request, self.template_name, {'invoice': invoice})

class InvoiceAddView(TemplateView):
	template_name = 'invoice/add_invoice.html'

	def get(self, request, *args, **kwargs):
		context = {
					'customer_form':CustomerForm(),
					'payment_form': PaymentForm(),
					'item_detail_form': ItemDetailForm(),
				  }
		return render(self.request, self.template_name, context)

	def post(self,request, *args, **kwargs):
		customer_form = CustomerForm(self.request.POST)
		payment_form = PaymentForm(self.request.POST)
		item_detail_form = ItemDetailForm(self.request.POST)

		if ( customer_form.is_valid() 
			and payment_form.is_valid()
			and item_detail_form.is_valid()):

			customer = customer_form.save(commit=False)
			
			customer.payment = payment_form.save()
			customer.item_detail = item_detail_form.save()
			customer.save()

			return redirect('invoices')
		else:
			context = {
					'customer_form':CustomerForm(),
					'payment_form': PaymentForm(),
					'item_detail_form': ItemDetailForm(),
				  }
		return render(self.request, self.template_name, context)

class InvoiceEditView(TemplateView):
	template_name = 'invoice/edit_invoice.html'

	def get(self, request, *args, **kwargs):
		invoice = get_object_or_404(Invoice, id=kwargs['invoice_id'])
		context = {
					'customer_form':CustomerForm(instance=invoice),
					'payment_form': PaymentForm(instance=invoice.payment),
					'item_detail_form': ItemDetailForm(instance=invoice.item_detail),
				  }
		return render(self.request, self.template_name, context)

	def post(self,request, *args, **kwargs):
		invoice = get_object_or_404(Invoice, id=kwargs['invoice_id'])
		customer_form = CustomerForm(self.request.POST, instance=invoice)
		payment_form = PaymentForm(self.request.POST, instance=invoice.payment)
		item_detail_form = ItemDetailForm(self.request.POST, instance=invoice.item_detail)

		if ( customer_form.is_valid() 
			and payment_form.is_valid()
			and item_detail_form.is_valid()):

			customer = customer_form.save(commit=False)
			
			customer.payment = payment_form.save()
			customer.item_detail = item_detail_form.save()
			customer.save()

			return redirect('invoices')
		else:
			context = {
						'customer_form':CustomerForm(instance=invoice),
						'payment_form': PaymentForm(instance=invoice.payment),
						'item_detail_form': ItemDetailForm(instance=invoice.item_detail),
						}
		return render(self.request, self.template_name, context)

class InvoiceDeleteView(TemplateView):
	def get(self, request, *args, **kwargs):
		invoice = get_object_or_404(Invoice, id=kwargs['invoice_id'])
		invoice.delete()
		return redirect('invoices')