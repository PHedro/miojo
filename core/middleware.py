import json

from django.utils import timezone

from core.models import BreadCrumbs


class HanselAndGretelMiddleware(object):
    def process_request(self, request):
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
        _get = request.GET
        if 'password' in _get.keys():
            _get.update({'password': '*******'})
        params.update({'get': json.dumps(_get)})
        _post = request.POST
        if 'password' in _post.keys():
            _post.update({'password': '*******'})
        params.update({'post': json.dumps(_post)})
        BreadCrumbs.objects.create(**params)
