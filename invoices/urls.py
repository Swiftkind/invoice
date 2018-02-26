from django.urls import path
from invoices.views import (
    IndexView,
    InvoiceAjaxView,
    InvoiceView,
    InvoiceDeleteView,
    InvoiceEmailView,
    MakeInvoiceView,
    PdfPreview,
    UpdateInvoiceForm,
    ) 


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('invoices/', InvoiceView.as_view(), name='invoices'),
    path('invoice/edit/<int:invoice_id>/<int:totalForm>/', UpdateInvoiceForm.as_view()
                                                         , name='invoice_edit'),
    path('invoice/delete/<int:invoice_id>/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoice/send_email/<int:invoice_id>/', InvoiceEmailView.as_view(), name='invoice_email'),
    path('invoice/pdf/<int:invoice_id>/', PdfPreview.as_view(), name='invoice_pdf'),
    #make invoice for client
    path('clients/make_invoice/<int:client_id>/', MakeInvoiceView.as_view(), name='make_invoice'),
    #ajax
    path('invoice/ajax/view/<int:invoice_id>/', InvoiceAjaxView.as_view(), name='invoice_ajax'),
]