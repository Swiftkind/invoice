from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404, redirect


from clients.models import Client



class UserIsOwnerMixin(AccessMixin):
    """Check ownership request 
    """
    def dispatch(self, *args, **kwargs):
        """ Request ownership check
        """
        client = get_object_or_404(Client, id=kwargs['client_id'])
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user != client.owner:
            return redirect('index')
        return super().dispatch(self.request, *args, **kwargs)