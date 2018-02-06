from django.urls import path
from invoices.views import (
    IndexView, 
    InvoiceListView, 
    InvoiceView, 
    InvoiceAddView, 
    InvoiceEditView, 
    InvoiceDeleteView, 
    InvoiceEmailView, 
    PdfPreview, 
    MakeInvoiceView
    ) 


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('invoices/', InvoiceListView.as_view(), name='invoices'),
    path('invoice/view/<int:invoice_id>/', InvoiceView.as_view(), name='invoice_view'),
    path('invoice/add/', InvoiceAddView.as_view(), name='invoice_add'),
    path('invoice/edit/<int:invoice_id>/', InvoiceEditView.as_view(), name='invoice_edit'),
    path('invoice/delete/<int:invoice_id>/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoice/send_email/<int:invoice_id>/', InvoiceEmailView.as_view(), name='invoice_email'),
    path('invoice/pdf/<int:invoice_id>/', PdfPreview.as_view(), name='invoice_pdf'),
    #make invoice for client
    path('clients/make_invoice/<int:client_id>/', MakeInvoiceView.as_view(), name='make_invoice'),
]