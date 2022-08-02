from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .managers import OwnerManager
from .managers import SellerManager
from .managers import CustomerManager
from .managers import UserCustomManger
from django.conf import settings
from djmoney.models.fields import MoneyField
from djmoney.money import Money


# Create your models here.

class UserAccount(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        OWNER = "OWNER", "Owner"
        SELLER = "SELLER", "Seller"
        CUSTOMER = "CUSTOMER", "Customer"

    type = models.CharField(max_length=15, choices=Types.choices,
                            default=Types.ADMIN)

    objects = UserCustomManger()


    # There is email and username and other field by default
    # but at least you should fill the username and the password


class Owner(models.Model):
    objects = OwnerManager()
    account = models.OneToOneField(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   )

    def __str__(self):
        return self.account.username

    def get_owner_mobiles(self):
        return self.mobile_set.select_related('owner').all()


class Seller(models.Model):
    objects = SellerManager()
    mobiles = models.ManyToManyField(to='products.Mobile', blank=True, default=None)
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # THE OWNER CAN JUST HAS ONE SELLER
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username


class Customer(models.Model):
    objects = CustomerManager()
    purchases = models.ManyToManyField(to='products.Mobile', blank=True, default=None)
    wallet = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency='USD',
        default=Money(1000, 'USD'),
    )

    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username

    def buy_mobile(self, mobile):
        self.wallet -= mobile.price
        self.purchases.add(mobile)
        self.save()
