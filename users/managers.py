from django.db import models
from django.contrib.auth.models import UserManager


class OwnerManager(UserManager):

    def get_queryset(self):
        from .models import UserAccount
        return super().get_queryset().filter(type=UserAccount.Types.OWNER)


class SellerManager(UserManager):

    def get_queryset(self):
        from .models import UserAccount
        return super().get_queryset().filter(type=UserAccount.Types.SELLER)


class CustomerManager(UserManager):

    def get_queryset(self):
        from .models import UserAccount
        return super().get_queryset().filter(type=UserAccount.Types.CUSTOMER)
