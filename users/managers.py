from django.db import models
from django.contrib.auth.models import UserManager


class UserCustomManger(UserManager):
    pass


class OwnerManager(UserManager):
    pass


class SellerManager(UserManager):
    pass


class CustomerManager(UserManager):
    pass
