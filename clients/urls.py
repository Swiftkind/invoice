from django.urls import path
from clients import views

c_id = '<int:client_id>'

urlpatterns = [
	path('clients/'              , views.ClientsView.as_view(),   name='clients'      ),
	path('client/view/'+c_id+'/'  , views.ClientViewView.as_view(),  name='client_view'  ),
	path('client/add/'           , views.ClientAddView.as_view(),  name='client_add'   ),
	path('client/edit/'+c_id+'/'  , views.ClientEditView.as_view(),  name='client_edit'  ),
	path('client/delete/'+c_id+'/', views.ClientDeleteView.as_view(),name='client_delete'),
]