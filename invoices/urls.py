from django.urls import path
from invoices.views import *

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('invoices/', InvoiceListView.as_view(),     name='invoices'      ),
	path('invoice/view/<int:invoice_id>/', InvoiceView.as_view(),  name='invoice_view'  ),
	path('invoice/add/', InvoiceAddView.as_view(),   name='invoice_add'   ),
	path('invoice/edit/<int:invoice_id>/', InvoiceEditView.as_view(),  name='invoice_edit'  ),
	path('invoice/delete/<int:invoice_id>/', InvoiceDeleteView.as_view(),name='invoice_delete'),
	path('invoice/pdf/<int:user_id>/', GeneratePdf.as_view(),   name='invoice_pdf'   ),
	path('clients/make_invoice/<int:client_id>/', MakeInvoiceView.as_view(),   name='make_invoice'   ),
	path('invoice/send_email/<int:invoice_id>/', InvoiceEmailView.as_view(), name='email'),
	path('pdf', PDF.as_view(),name='pdf')
]