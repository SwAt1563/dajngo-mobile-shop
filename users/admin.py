from django.contrib import admin
from .models import Owner
from .models import Seller
from .models import Customer
from .models import UserAccount


# Register your models here.

class OwnerAdmin(admin.ModelAdmin):
    pass


class SellerAdmin(admin.ModelAdmin):
    pass


class CustomerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Owner, OwnerAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(UserAccount)
