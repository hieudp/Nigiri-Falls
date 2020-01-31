from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('increase/', views.increase, name='increasecart'),
    path('decrease/', views.decrease, name='decreasecart'),
]
