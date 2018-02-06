from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404, redirect


from items.models import Item



class UserIsOwnerMixin(AccessMixin):
    """Check ownership request 
    """
    def dispatch(self, *args, **kwargs):
        """ Request ownership check
        """
        item = get_object_or_404(Item, id=kwargs['item_id'])
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user != item.owner:
            return redirect('index')
        return super().dispatch(self.request, *args, **kwargs)