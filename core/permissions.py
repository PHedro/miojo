from django.core.exceptions import SuspiciousOperation


class GateKeeper(object):
    @staticmethod
    def _merge_params(base, *param_dicts):
        for _dict in param_dicts:
            for key, value in _dict.items():
                if key in base and value != base[key]:
                    raise SuspiciousOperation
                base[key] = value

    def check_request(self, request, *args, **kwargs):
        self._merge_params(kwargs, request.GET, request.POST)
        return self.check_permission(request.user, *args, **kwargs)

    def check_permission(self, user, *args, **kwargs):
        raise NotImplementedError


class AdminGateKeeper(GateKeeper):
    def check_permission(self, user, *args, **kwargs):
        return user.is_superuser and user.is_verified()
