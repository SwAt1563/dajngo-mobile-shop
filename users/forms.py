from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import UserAccount
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    # because we don't want to let the guest register as seller or admin
    type = forms.ChoiceField(choices=(('OWNER', 'Owner'), ('CUSTOMER', 'Customer')))

    class Meta(UserCreationForm.Meta):
        model = UserAccount
        fields = UserCreationForm.Meta.fields + ('type',)

    # for create owner or customer object after create the user
    def save(self, commit=True):
        from .models import Owner, Customer
        user = super(CustomUserCreationForm, self).save(commit=True)

        if user.type == 'OWNER' or user.type == 'Owner':
            Owner.objects.create(account=user)
        elif user.type == 'CUSTOMER' or user.type == 'Customer':
            Customer.objects.create(account=user)

        return user


class CreateSellerByOwnerForm(ModelForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    # for just show the mobiles that available for current owner
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateSellerByOwnerForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['mobiles'].queryset = user.owner.get_owner_mobiles()

    class Meta:
        from .models import Seller
        model = Seller
        fields = ('username', 'password', 'mobiles')
