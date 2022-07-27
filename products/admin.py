from django.contrib import admin
from products.models import Mobile
from products.models import Category


# Register your models here.

class MobileAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Mobile, MobileAdmin)
admin.site.register(Category, CategoryAdmin)
