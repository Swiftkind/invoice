from django.urls import path
from clients import views


urlpatterns = [
	path('clients/', views.ClientListView.as_view(), name='clients'),
	path('client/view/<int:client_id>/', views.ClientView.as_view(), name='client_view'),
	path('client/add/', views.ClientAddView.as_view(), name='client_add'),
	path('client/edit/<int:client_id>/', views.ClientEditView.as_view(), name='client_edit'),
	path('client/delete/<int:client_id>/', views.ClientDeleteView.as_view(), name='client_delete'),
]