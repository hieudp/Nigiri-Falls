from django.urls import path

from . import views

urlpatterns = [
    path('', views.add_dish, name='addDish'),
    path('addCategori/', views.add_categori, name='addCategori'),
]
