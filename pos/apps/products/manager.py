from apps.core.services.status import *


class ProductQuerySet(models.QuerySet):
    """
    product__title
    """
    def search(self, query=None):
        qs = self
        if query is not None:
            qs = qs.filter(title__icontains=query).distinct()
            # qs = qs.filter(
            #     Q(product__title__icontains=query) |
            # ).distinct()
        return qs


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

