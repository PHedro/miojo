from django.core.exceptions import ObjectDoesNotExist


class DeleteNotPermitted(Exception):
    pass


class ObjectIsDeleted(ObjectDoesNotExist):
    pass
