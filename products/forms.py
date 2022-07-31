from django import forms
from .models import Category

class PriceForm(forms.Form):
    minimum = forms.FloatField()
    maximum = forms.FloatField()


class CategoryForm(forms.Form):
    choices = [(option, option) for option in
               Category.objects.list_the_categories() \
                   .values_list('name', flat=True)]
    category = forms.ChoiceField(choices=choices)
