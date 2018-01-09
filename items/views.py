from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from items.models import Item
from items.forms import ItemForm
# Create your views here.

class ItemsView(TemplateView):
	template_name = 'items/all_item.html'

	def get(self, request, *args, **kwargs):
		return render(self.request, self.template_name, {'items': Item.objects.all()})

class ItemsViewView(TemplateView):
	template_name = 'items/view_item.html'

	def get(self, request, *args, **kwargs):
		item = get_object_or_404(Item, id=kwargs['item_id'])
		return render(self.request, self.template_name, {'item': item})

class ItemsAddView(TemplateView):
	template_name = 'items/add_item.html'

	def get(self, request, *args, **kwargs):
		return render(self.request, self.template_name, {'item_form': ItemForm() })
	def post(self, request, *args, **kwargs):
		item_form = ItemForm(self.request.POST)
		if item_form.is_valid():
			item_form.save()
			return redirect('items')
		else:
			context = {'item_form': ItemForm() }
		return render(self.request, self.template_name, context)

class ItemsEditView(TemplateView):
	template_name = 'items/edit_item.html'

	def get(self, request, *args, **kwargs):
		item = get_object_or_404(Item, id=kwargs['item_id'])
		return render(self.request, self.template_name, {'item_form': ItemForm(instance=item) })
	def post(self, request, *args, **kwargs):
		item = get_object_or_404(Item, id=kwargs['item_id'])
		item_form = ItemForm(self.request.POST, instance=item)
		if item_form.is_valid():
			item_form.save()
			return redirect('items')
		else:
			context = {'item_form': ItemForm(self.request.POST, instance=item) }
		return render(self.request, self.template_name, context)

class ItemsDeleteView(TemplateView):
	def get(self, request, *args, **kwargs):
		item = get_object_or_404(Item, id=kwargs['item_id'])
		item.delete()
		return redirect('items')
