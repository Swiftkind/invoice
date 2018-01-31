from django.urls import path
from invoices import views



urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoices'),
    path('invoice/view/<int:invoice_id>/', views.InvoiceView.as_view(), name='invoice_view'),
    path('invoice/add/', views.InvoiceAddView.as_view(), name='invoice_add'),
    path('invoice/edit/<int:invoice_id>/', views.InvoiceEditView.as_view(), name='invoice_edit'),
    path('invoice/delete/<int:invoice_id>/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoice/send_email/<int:invoice_id>/', views.InvoiceEmailView.as_view(), name='email'),

    path('clients/make_invoice/<int:client_id>/', views.MakeInvoiceView.as_view(), name='make_invoice'),
]