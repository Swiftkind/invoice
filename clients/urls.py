from django.urls import path
from clients.views import ClientsView,ClientViewView,ClientAddView, ClientEditView,ClientDeleteView

c_id = '<int:client_id>'

urlpatterns = [
	path('clients/'               , ClientsView.as_view(),     name='clients'      ),
	path('client/view/'+c_id+'/'  , ClientViewView.as_view(),  name='client_view'  ),
	path('client/add/'            , ClientAddView.as_view(),   name='client_add'   ),
	path('client/edit/'+c_id+'/'  , ClientEditView.as_view(),  name='client_edit'  ),
	path('client/delete/'+c_id+'/', ClientDeleteView.as_view(),name='client_delete'),
]