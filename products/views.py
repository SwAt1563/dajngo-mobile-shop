from django.shortcuts import render
from django.views.generic import ListView
from .models import Mobile
from .models import Category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from users.models import Customer
from django.urls import reverse
from .forms import PriceForm
from .forms import CategoryForm
from users.models import UserAccount
from django.http import HttpResponseRedirect


# Create your views here.


def is_customer(user):
    try:
        return user.is_authenticated and user.type == 'CUSTOMER'
    except UserAccount.DoesNotExist:
        return False


class ParametersMixin(object):
    paginate_by = 8


class MobileListView(ParametersMixin, ListView):
    template_name = 'products/home.html'  # redirect template
    context_object_name = 'list_objects'  # name of mobiles parameter that we can access in template

    def get(self, request, *args, **kwargs):
        # extra context that we can use it in template
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
        elif category_form.is_valid():
            self.extra_context = {
                'category_form': category_form,
                'price_form': PriceForm
            }
            self.extra_context.update({
                'category': category_form.cleaned_data['category']
            })
        return super(MobileListView, self).get(request, *args, **kwargs)

    # what we want to put in 'list_objects'
    def get_queryset(self):
        if self.request.method == 'POST':
            if self.extra_context.get('category'):
                return Category.objects.filter(name=self.extra_context['category']) \
                    .first() \
                    .get_mobiles_based_on_category()
            minimum = self.extra_context['minimum']
            maximum = self.extra_context['maximum']
            return Mobile.objects.get_mobiles_based_on_price(minimum, maximum)
        return Mobile.objects.list_active_mobiles()


def mobile(request, mobile_id):
    obj = Mobile.objects.get(pk=mobile_id)
    return render(request, 'products/mobile.html', {'mobile': obj})


@login_required(login_url='users:login')
@user_passes_test(is_customer, login_url='users:logout')
def buy_mobile(request, mobile_id):
    mobile = get_object_or_404(Mobile, pk=mobile_id)
    customer = get_object_or_404(Customer, pk=request.user.customer.pk)

    def check_process(m, c):
        if m.amount <= 0 or m.price > c.wallet:
            return False
        return True

    if check_process(mobile, customer):
        mobile.dec_the_amount()
        customer.buy_mobile(mobile)
        if not mobile.is_active:
            return HttpResponseRedirect(reverse('products:home'))
    return HttpResponseRedirect(reverse('products:mobile', args=(mobile.id,)))
