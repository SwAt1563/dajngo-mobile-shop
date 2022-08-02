from django.db import models


# for mange Category.objects queryset
class CategoryQuerySet(models.QuerySet):
    def order_by_name(self):
        return self.order_by('name')

    def get_mobiles_by_category(self, category):
        return self.get(category).get_mobiles_by_category()


# create our methods for use it as Category.objects.our_function()
class CategoryManager(models.Manager):

    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def list_the_categories(self):
        return self.get_queryset().order_by_name()

    def get_the_mobiles_of_category(self, category):
        return self.get_queryset().get_mobiles_by_category(category)


class MobileQuerySet(models.QuerySet):
    def get_range(self, minimum=0.0, maximum=100000000.0):
        return self.filter(is_active=True, price__gte=minimum, price__lte=maximum)

    def get_filtering_mobiles(self):
        return self.filter(is_active=True)


class MobileManager(models.Manager):

    def get_queryset(self):
        return MobileQuerySet(self.model, using=self._db)

    def get_mobiles_based_on_price(self, minimum, maximum):
        return self.get_queryset().get_range(minimum, maximum)

    def list_active_mobiles(self):
        return self.get_queryset().get_filtering_mobiles()
