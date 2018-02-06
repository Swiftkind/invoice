from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404, redirect


from users.models import User



class UserIsOwnerMixin(AccessMixin):
    """Check ownership request 
    """
    def dispatch(self, *args, **kwargs):
        """ Request ownership check
        """
        user = get_object_or_404(User, id=kwargs['user_id'])
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user.email != user.email:
            return redirect('index')
        return super().dispatch(self.request, *args, **kwargs)