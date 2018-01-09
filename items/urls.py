from django.urls import path
from items import views

urlpatterns = [
	path('items/', views.ItemsView.as_view(), name='items'),
	path('items/view/<int:item_id>/', views.ItemsViewView.as_view(), name='item_view'),
	path('items/add/', views.ItemsAddView.as_view(), name='item_add'),
	path('items/edit/<int:item_id>/', views.ItemsEditView.as_view(), name='item_edit'),
	path('items/delete/<int:item_id>/', views.ItemsDeleteView.as_view(), name='item_delete' ),
]