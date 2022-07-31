from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Mobile
from .models import Category

from django.urls import reverse
from .forms import PriceForm
from .forms import CategoryForm

from django.http import HttpResponseRedirect


# Create your views here.


# def home(request):
#     return

class Parameters(object):
    paginate_by = 8


class MobileListView(Parameters, ListView):

    template_name = 'products/home.html'
    context_object_name = 'list_objects'

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'price_form': PriceForm,
            'category_form': CategoryForm,
        }
        return super(MobileListView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        price_form = PriceForm(request.POST)
        category_form = CategoryForm(request.POST)
        if price_form.is_valid():
            self.extra_context = {
                'price_form': price_form,
                'category_form': CategoryForm
            }
            self.extra_context.update({
                'minimum': price_form.cleaned_data['minimum'],
                'maximum': price_form.cleaned_data['maximum'],
            })
        if category_form.is_valid():
            self.extra_context = {
                'category_form': category_form,
                'price_form': PriceForm
            }
            self.extra_context.update({
                'category': category_form.cleaned_data['category']
            })
        return super(MobileListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.method == 'POST':
            if self.extra_context.get('category'):
                return Category.objects.filter(name=self.extra_context['category'])\
                    .first()\
                    .get_mobiles_based_on_category()
            minimum = self.extra_context['minimum']
            maximum = self.extra_context['maximum']
            return Mobile.objects.get_mobiles_based_on_price(minimum, maximum)
        return Mobile.objects.list_active_mobiles()


def mobile(request, mobile_id):
    obj = Mobile.objects.get(pk=mobile_id)
    return render(request, 'products/mobile.html', {'mobile': obj})
