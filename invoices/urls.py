from django.urls import path
from invoices.views import PDF,InvoiceEmailView,MakeInvoiceView,IndexView,InvoicesView,InvoiceViewView,InvoiceAddView, InvoiceEditView,InvoiceDeleteView,InvoicePdfView



in_id = '<int:invoice_id>'

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('invoices/'               , InvoicesView.as_view(),     name='invoices'      ),
	path('invoice/view/'+in_id+'/'  , InvoiceViewView.as_view(),  name='invoice_view'  ),
	path('invoice/add/'            , InvoiceAddView.as_view(),   name='invoice_add'   ),
	path('invoice/edit/'+in_id+'/'  , InvoiceEditView.as_view(),  name='invoice_edit'  ),
	path('invoice/delete/'+in_id+'/', InvoiceDeleteView.as_view(),name='invoice_delete'),
	path('invoice/pdf/<int:user_id>/', InvoicePdfView.as_view(),   name='invoice_pdf'   ),
	path('clients/make_invoice/<int:client_id>/'  , MakeInvoiceView.as_view(),   name='make_invoice'   ),
	path('invoice/send_email/'+in_id+'/', InvoiceEmailView.as_view(), name='email'),
	path('pdf', PDF.as_view(),name='pdf')
]