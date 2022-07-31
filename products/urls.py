from django.urls import path
from products import views

app_name = 'products'
urlpatterns = [
        path('', views.MobileListView.as_view(), name='home'),
        path('mobile/<int:mobile_id>/', views.mobile, name='mobile'),
    ]