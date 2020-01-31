from django.urls import path

from . import views

urlpatterns = [
    path('', views.orders_view, name='orders'),
    path('delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('update/<int:pk>/', views.order_update, name='order_update'),
    path('manage/', views.manage_orders, name='order_manage'),
]
