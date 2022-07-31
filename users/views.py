from django.shortcuts import render


# Create your views here.


def dashboard(request):
    render(request, 'users/dashboard.html')


def login(request):
    pass
