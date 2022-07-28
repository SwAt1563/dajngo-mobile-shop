from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Mobile
from django.urls import reverse


# Create your views here.


# def home(request):
#     return

class MobileListView(ListView):
    paginate_by = 8
    template_name = 'products/home.html'

    def get_queryset(self):
        return Mobile.objects.list_active_mobiles()


def mobile(request, mobile_id):
    obj = Mobile.objects.get(pk=mobile_id)
    return render(request, 'products/mobile.html', {'mobile': obj})
