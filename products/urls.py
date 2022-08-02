from django.urls import path
from products import views

# for make it easy by calling the views by products:name
app_name = 'products'
urlpatterns = [
        path('', views.MobileListView.as_view(), name='home'),
        path('mobile/<int:mobile_id>/', views.mobile, name='mobile'),
        path('buy_mobile/<int:mobile_id>/', views.buy_mobile, name='buy_mobile'),

]