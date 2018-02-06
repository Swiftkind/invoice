from django.urls import path
from items.views import ItemListView, ItemView, ItemAddView, ItemEditView, ItemDeleteView



urlpatterns = [
    path('items/', ItemListView.as_view(), name='items'),
    path('item/view/<int:item_id>/', ItemView.as_view(), name='item_view'),
    path('item/add/', ItemAddView.as_view(), name='item_add'),
    path('item/edit/<int:item_id>/', ItemEditView.as_view(), name='item_edit'),
    path('item/delete/<int:item_id>/', ItemDeleteView.as_view(), name='item_delete'),

]