from django.contrib.admin.utils import NestedObjects
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import signals
from django.utils import timezone


class BaseQueryset(models.QuerySet):
    def _wrap(self, func, args, kwargs):
        try:
            result = func(*args, **kwargs)
        except ObjectDoesNotExist:
            for node in self.query.where.children[:]:
                if hasattr(node, 'children'):
                    for child in node.children:
                        if child.lhs.attname == 'deleted':
                            node.children.remove(child)
                    if not node.children:
                        self.query.where.children.remove(node)
            q = super(BaseQueryset, self).filter(*args, **kwargs)
            if q.exists():
                raise ObjectDoesNotExist('Objeto existe porém foi deletado.')
            else:
                raise ObjectDoesNotExist('Objeto não existe.')
        return result

    def get(self, *args, **kwargs):
        return self._wrap(
            super(BaseQueryset, self).get, args, kwargs
        )

    def get_or_create(self, *args, **kwargs):
        return self._wrap(
            super(BaseQueryset, self).get_or_create, args, kwargs
        )

    def delete(self, cascade=True, **kwargs):
        if cascade:
            for obj in self.all():
                obj.delete()

        return self.update(
            deleted=True,
            deleted_at=timezone.now()
        )

    def all(self, exclude_deleted=True):
        q = self._clone()
        if exclude_deleted:
            q = q.exclude(deleted=True)
        return q


class BaseManager(models.Manager):
    queryset_class = BaseQueryset
    use_for_related_fields = True

    def get_queryset(self, exclude_deleted=True):
        q = self.queryset_class(self.model)
        if hasattr(self, 'default_filters'):
            q = q.filter(**self.default_filters)
        if exclude_deleted:
            q = q.exclude(deleted=True)
        return q

    def full_all(self):
        return self.get_queryset(exclude_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None)
    deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True

    def delete(self, cascade=True, **kwargs):
        if cascade:
            collector = NestedObjects(using='default')
            collector.collect([self])
            field_updates = collector.field_updates
            for cls, to_update in field_updates.iteritems():
                for (field, value), instances in to_update.iteritems():
                    cls.objects.filter(
                        pk__in={o.pk for o in instances}
                    ).update(**{field.attname: value})
            for klass, objs in collector.data.iteritems():
                try:
                    klass._meta.get_field('deleted')
                except models.FieldDoesNotExist:
                    pass
                else:
                    klass.objects.filter(pk__in={o.pk for o in objs}).update(
                        deleted=True, deleted_at=timezone.now()
                    )
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
        signals.post_delete.send(
            sender=self.__class__,
            instance=self
        )


class BreadCrumbs(BaseModel):
    user = models.CharField(
        max_length=300, blank=True, null=True, db_index=True
    )
    user_agent = models.CharField(
        max_length=500, blank=True, null=True
    )
    ip = models.CharField(
        max_length=100, blank=True, null=True, db_index=True
    )
    method = models.CharField(
        max_length=10, blank=True, null=True, db_index=True
    )
    url = models.CharField(
        max_length=1000, blank=True, null=True
    )
    referer = models.CharField(
        max_length=1000, blank=True, null=True
    )
    get = models.TextField(
        blank=True, null=True
    )
    post = models.TextField(
        blank=True, null=True
    )
