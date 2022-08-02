from django.contrib import admin
from products.models import Mobile
from products.models import Category


# Register your models here.

# for make edit on default view of model in administration
class MobileAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


# for show the models in administration page
admin.site.register(Mobile, MobileAdmin)
admin.site.register(Category, CategoryAdmin)
