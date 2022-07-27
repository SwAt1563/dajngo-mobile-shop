from django.db import models
from django.contrib.postgres.fields import ArrayField
from products.managers import MobileManager


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    categories = models.ManyToManyField("self", null=True, blank=True)

    def __str__(self):
        return self.name


class Mobile(models.Model):
    name = models.CharField(max_length=20)
    size = models.IntegerField()
    price = models.FloatField()
    category = models.ForeignKey(Category, default=1, on_delete=models.SET_DEFAULT)
    about = ArrayField(models.CharField(max_length=100, null=True, blank=True), size=10)
    mobile_image = models.ImageField(null=True, blank=True, upload_to='mobiles_images/')

    objects = MobileManager()

    def __str__(self):
        return self.name
