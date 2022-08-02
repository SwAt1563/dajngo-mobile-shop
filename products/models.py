from django.db import models
from django.contrib.postgres.fields import ArrayField
from products.managers import MobileManager
from products.managers import CategoryManager
from users.models import Owner
from djmoney.models.fields import MoneyField
from djmoney.money import Money


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', default=None, null=True, blank=True, related_name='nested_category',
                               on_delete=models.CASCADE)

    objects = CategoryManager()

    def __str__(self):
        return self.name

    # for get the mobiles under the category included its children's mobiles
    def get_mobiles_based_on_category(self):
        if self.nested_category.exists():
            current_mobiles = self.mobile_set.select_related('category').all()
            for children in self.nested_category.select_related('parent').all():
                current_mobiles = current_mobiles.union(children.get_mobiles_based_on_category())

            return current_mobiles
        return self.mobile_set.select_related('category').all().filter(is_active=True)


class Mobile(models.Model):
    name = models.CharField(max_length=20)
    size = models.IntegerField()
    price = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency='USD',
        default=Money(0, 'USD')
    )
    category = models.ForeignKey(Category, default=1, on_delete=models.SET_DEFAULT)
    about = ArrayField(models.CharField(max_length=100, null=True, blank=True), size=10)
    mobile_image = models.ImageField(null=True, blank=True, upload_to='mobiles_images/')
    amount = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    objects = MobileManager()

    def inc_the_amount(self):
        if not self.is_active:
            self.is_active = True
        self.amount += 1
        self.save()

    def dec_the_amount(self):
        if not self.is_active or self.amount == 0:
            raise Exception('There is no any mobiles in the shop')
        self.amount -= 1
        if self.amount == 0:
            self.is_active = False
        self.save()

    # for delete the image storage
    def delete(self, using=None, keep_parents=False):
        self.mobile_image.delete()
        super(Mobile, self).delete()

    def __str__(self):
        return self.name
