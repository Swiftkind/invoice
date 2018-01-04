from django.urls import path
from contacts import views

urlpatterns = [
	path('contacts/', views.ContactsView.as_view(), name='contacts'),
	path('contact/view/<int:contact_id>', views.ContactViewView.as_view(), name='contact_view'),
	path('contact/add/', views.ContactAddView.as_view(), name='contact_add'),
	path('contact/edit/<int:contact_id>', views.ContactEditView.as_view(), name='contact_edit'),
	path('contact/delete/<int:contact_id>', views.ContactDeleteView.as_view(), name='contact_delete'),
]