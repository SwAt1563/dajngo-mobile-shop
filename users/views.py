from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from products.models import Mobile
from .models import UserAccount
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Owner, Seller
from .forms import CreateSellerByOwnerForm
from django.contrib.auth.hashers import make_password
from products.views import ParametersMixin
from django.views.generic import ListView


def is_seller(user):
    try:
        return user.is_authenticated and user.type == 'SELLER'
    except UserAccount.DoesNotExist:
        return False


def is_owner(user):
    try:
        return user.is_authenticated and user.type == 'OWNER'
    except UserAccount.DoesNotExist:
        return False


# Create your views here.


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, ParametersMixin, ListView):
    login_url = 'users:login'
    template_name = 'users/dashboard.html'
    context_object_name = 'list_mobiles'

    def test_func(self):
        return is_owner(self.request.user) or is_seller(self.request.user)

    # return the available mobiles depend on the current user
    def get_queryset(self):
        if is_owner(self.request.user):
            owner = get_object_or_404(Owner, pk=self.request.user.owner.pk)
            return owner.get_owner_mobiles()
        else:
            seller = get_object_or_404(Seller, pk=self.request.user.seller.pk)
            return seller.mobiles.all()


# registration just for customer or owner
def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html',
                      {'form': CustomUserCreationForm}
                      )
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('users:dashboard'))


@login_required(login_url='users:login')
@user_passes_test(lambda user: is_seller(user) or is_owner(user), login_url='users:logout')
def active(request, mobile_id):
    mobile = get_object_or_404(Mobile, pk=mobile_id)
    if mobile.is_active:
        mobile.is_active = False
    else:
        mobile.is_active = True
    mobile.save()
    return HttpResponseRedirect(reverse('users:dashboard'))


@login_required(login_url='users:login')
@user_passes_test(is_owner, login_url='users:logout')
def delete(request, mobile_id):
    mobile = get_object_or_404(Mobile, pk=mobile_id)
    mobile.delete()
    return HttpResponseRedirect(reverse('users:dashboard'))


class MobileCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mobile
    fields = ("name", "size", "price", "category", "about",
              "mobile_image", "amount", "is_active")
    login_url = 'users:login'
    template_name = 'users/add_mobile.html'

    def get_success_url(self):
        return reverse('users:dashboard')

    # for make relation between the creation mobile with current owner
    def form_valid(self, form):
        owner = get_object_or_404(Owner, pk=self.request.user.owner.pk)
        form.instance.owner = owner
        return super(MobileCreate, self).form_valid(form)

    def test_func(self):
        return is_owner(self.request.user)


class SellerCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Seller
    form_class = CreateSellerByOwnerForm
    login_url = 'users:login'
    template_name = 'users/add_seller.html'

    def get_form_kwargs(self):
        kwargs = super(SellerCreate, self).get_form_kwargs()

        if self.request.method == 'GET':
            kwargs.update({
                'user': self.request.user,
            })
        return kwargs

    def get_success_url(self):
        return reverse('users:dashboard')

    def form_valid(self, form):
        from .models import UserAccount
        owner = get_object_or_404(Owner, pk=self.request.user.owner.pk)
        form.instance.owner = owner
        new_user = UserAccount(
            username=form.cleaned_data['username'],
            password=make_password(form.cleaned_data['password']),  # for make encoding by use make_password
            type=UserAccount.Types.SELLER,
        )
        new_user.save()
        form.instance.account = new_user
        return super(SellerCreate, self).form_valid(form)

    def test_func(self):
        return is_owner(self.request.user)
