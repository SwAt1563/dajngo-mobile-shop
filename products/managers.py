from django.db import models


class MobileQuerySet(models.QuerySet):
    def get_range(self, minimum=0, maximum=100000000.0):
        return self.filter(price__bte=minimum, price__lte=maximum)


class MobileManager(models.Manager):

    def get_queryset(self):
        return MobileQuerySet(self.model, using=self._db)

    def get_mobiles_based_on_price(self, minimum, maximum):
        return self.get_queryset().get_range(minimum, maximum)
