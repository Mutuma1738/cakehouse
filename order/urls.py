from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/<int:product_id>/', views.order_cake, name='order_cake'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),

]
