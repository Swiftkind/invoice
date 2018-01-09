from django.urls import path
from invoice import views

urlpatterns = [
	path('invoices/', views.InvoiceView.as_view(), name='invoices'),
	path('invoice/add/', views.InvoiceAddView.as_view(), name='invoice_add'),
	path('invoice/view/<int:invoice_id>/', views.InvoiceViewView.as_view(), name='invoice_view'),
	path('invoice/edit/<int:invoice_id>/', views.InvoiceEditView.as_view(), name='invoice_edit'),
	path('invoice/delete/<int:invoice_id>/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),
]