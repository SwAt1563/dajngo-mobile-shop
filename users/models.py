from django.db import models
from django.contrib.auth.models import User
from .managers import OwnerManager
from .managers import SellerManager
from .managers import CustomerManager


# Create your models here.

# https://www.youtube.com/watch?v=f0hdXr2MOEA
# https://docs.djangoproject.com/en/4.1/topics/auth/default/#how-to-log-a-user-out
class UserAccount(User):
    is_superuser = False
    is_active = False
    is_staff = False

    class Types(models.TextChoices):
        OWNER = "OWNER", "Owner"
        SELLER = "SELLER", "Seller"
        CUSTOMER = "CUSTOMER", "Customer"

    type = models.CharField(max_length=15, choices=Types.choices,
                            default=Types.CUSTOMER)

    # There is email and username and other field by default
    # but at least you should fill the username and the password


class Owner(UserAccount):
    objects = OwnerManager()

    class Meta:
        proxy = False  # IF TRUE: then don't create new table, and use the User table
        permissions = [
            ("add_mobile", "add mobile"),
            ("delete_mobile", "delete mobile"),
            ("update_mobile", "update mobile"),
            ("show_mobile", "show mobile"),
            ("inactive_mobile", "inactive mobile"),
        ]

    # Owner.objects.create(username="x", email="y")
    # instead of
    # Owner.objects.create(username="x", email="y", type=User.Types.OWNER)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = UserAccount.Types.OWNER
        return super().save(*args, **kwargs)


class Seller(UserAccount):

    objects = SellerManager()
    mobiles = models.ManyToManyField(to='products.Mobile', blank=True, default=None)

    class Meta:
        proxy = False
        permissions = [
            ("show_mobile", "show mobile"),
            ("inactive_mobile", "inactive mobile"),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = UserAccount.Types.SELLER
        return super().save(*args, **kwargs)


class Customer(UserAccount):

    objects = CustomerManager()
    purchases = models.ManyToManyField(to='products.Mobile', blank=True, default=None)
    wallet = models.FloatField(default=1000.0)

    class Meta:
        proxy = False
        permissions = [
            ("buy_mobile", "buy mobile"),
            ("show_mobile", "show mobile"),
        ]

    def buy_mobile(self, mobile):
        self.wallet -= mobile.price
        self.purchases.add(mobile)
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = UserAccount.Types.CUSTOMER
        return super().save(*args, **kwargs)
