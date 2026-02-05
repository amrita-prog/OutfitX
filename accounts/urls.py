from django.urls import path
from . import views

urlpatterns = [
    path('signup/admin/', views.admin_signup, name='admin_signup'),
    path('signup/sales/', views.sales_executive_signup, name='sales_executive_signup'),
    path('signup/inventory/', views.inventory_manager_signup, name='inventory_manager_signup'),
    path('login/', views.custom_login, name='login'),
]