from django.urls import path
from clients.views import ClientListView, ClientView, ClientAddView, ClientEditView, ClientDeleteView, ClientInvoice


urlpatterns = [
    path('clients/', ClientListView.as_view(), name='clients'),
    path('client/view/<int:client_id>/', ClientView.as_view(), name='client_view'),
    path('client/add/', ClientAddView.as_view(), name='client_add'),
    path('client/edit/<int:client_id>/', ClientEditView.as_view(), name='client_edit'),
    path('client/delete/<int:client_id>/', ClientDeleteView.as_view(), name='client_delete'),

    path('client/invoice/<int:client_id>/', ClientInvoice.as_view(), name='client_invoice')
]