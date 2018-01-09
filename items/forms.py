from django.forms import ModelForm, RadioSelect, Textarea
from items.models import Item						
from custom.choices import ITEM_TYPE

class ItemForm(ModelForm):
	class Meta:
		model  = Item
		fields = '__all__'
		widgets = {
			'item_type': RadioSelect(choices=ITEM_TYPE),
			'description': Textarea(),
		}
