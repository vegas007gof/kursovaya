from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/new/', views.sale_create, name='sale_create'),
    path('sales/', views.sales_list, name='sales_report'),
    path('sales/report/', views.sales_report, name='sales_report'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('add_product/', views.add_product, name='add_product'),
    path('sales_list/', views.sales_list, name='sales_list'),
]

