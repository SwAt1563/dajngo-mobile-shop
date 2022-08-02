from django.urls import path, re_path, include
from users import views

app_name = 'users'
urlpatterns = [
    path('control_panel/', views.DashboardView.as_view(), name='dashboard'),
    path("", include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('control_panel/add_mobile', views.MobileCreate.as_view(), name='add_mobile'),
    path('control_panel/delete_mobile/<int:mobile_id>/', views.delete, name='delete_mobile'),
    path('control_panel/mobile_status/<int:mobile_id>/', views.active, name='mobile_status'),
    path('control_panel/add_seller', views.SellerCreate.as_view(), name='add_seller'),
]
