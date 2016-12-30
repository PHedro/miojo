from django.core.exceptions import PermissionDenied
from django.views import generic

from core.permissions import AdminGateKeeper


class BaseView(generic.View):
    permissions = AdminGateKeeper()
    permissions_method = all  # or any

    def dispatch(self, request, *args, **kwargs):
        permissions = self.permissions
        if not isinstance(permissions, (list, tuple, set)):
            permissions = (permissions,)
        if self.permissions_method(
            permission.check_request(request, *args, **kwargs)
            for permission in permissions
        ):
            return super(BaseView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied
