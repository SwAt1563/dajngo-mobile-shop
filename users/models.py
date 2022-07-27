from django.db import models
from django.contrib.auth.models import User
from .managers import OwnerManager
from .managers import SellerManager
from .managers import CustomerManager
from django.urls import reverse

# Create your models here.

# https://www.youtube.com/watch?v=f0hdXr2MOEA
# https://docs.djangoproject.com/en/4.1/topics/auth/default/#how-to-log-a-user-out
class UserAccount(User):
    is_superuser = False
    is_active = False
    is_staff = False
    is_owner = False
    is_seller = False
    is_customer = False

    class Types(models.TextChoices):
        OWNER = "OWNER", "Owner"
        SELLER = "SELLER", "Seller"
        CUSTOMER = "CUSTOMER", "Customer"

    type = models.CharField(max_length=15, choices=Types.choices,
                            default=Types.CUSTOMER)

    # There is email and username by default


class Owner(UserAccount):
    is_owner = True
    objects = OwnerManager()

    class Meta:
        proxy = True  # For don't create new table, and use the User table
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
    is_seller = True
    objects = SellerManager()

    class Meta:
        proxy = True
        permissions = [
            ("show_mobile", "show mobile"),
            ("inactive_mobile", "inactive mobile"),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = UserAccount.Types.SELLER
        return super().save(*args, **kwargs)


class Customer(UserAccount):
    is_customer = True
    objects = CustomerManager()

    class Meta:
        proxy = True
        permissions = [
            ("buy_mobile", "buy mobile"),
            ("show_mobile", "show mobile"),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = UserAccount.Types.CUSTOMER
        return super().save(*args, **kwargs)
