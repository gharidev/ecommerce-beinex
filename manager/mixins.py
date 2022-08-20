from django.contrib.auth.mixins import AccessMixin
from core.models import User


class ManagerRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a manager."""
    
    permission_denied_message = 'You do not have enough privileges to access this page.'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif request.user.type != User.Types.MANAGER:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)