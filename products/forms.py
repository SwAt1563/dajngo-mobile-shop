from django import forms
from .models import Category

# Custom form for search about mobiles depend on price
class PriceForm(forms.Form):
    minimum = forms.FloatField()
    maximum = forms.FloatField()


# for get select form of exists categories
class CategoryForm(forms.Form):
    choices = [(option, option) for option in
               Category.objects.list_the_categories() \
                   .values_list('name', flat=True)]
    category = forms.ChoiceField(choices=choices)
