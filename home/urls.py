from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('increase/', views.increase, name='increase'),
    path('decrease/', views.decrease, name='decrease'),
    path('set_categori/', views.set_categori, name='set_categori')
]
