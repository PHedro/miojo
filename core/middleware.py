import json

from copy import copy
from django.utils import timezone

from core.models import BreadCrumbs


def hansel_and_gretel_middleware(get_response):
    def breadcrumbs_path(request):
        params = {
            'user': request.user,
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'ip': request.META.get('REMOTE_ADDR'),
            'url': request.path,
            'referer': request.META.get('HTTP_REFERER'),
            'method': request.META.get('REQUEST_METHOD'),
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'deleted_at': None,
            'deleted': False
        }
        _get = copy(request.GET)
        if 'password' in _get.keys():
            _get.update({'password': '*******'})
        params.update({'get': json.dumps(_get)})
        _post = copy(request.POST)
        if 'password' in _post.keys():
            _post.update({'password': '*******'})
        params.update({'post': json.dumps(_post)})
        BreadCrumbs.objects.create(**params)
        response = get_response(request)
        return response
    return breadcrumbs_path
