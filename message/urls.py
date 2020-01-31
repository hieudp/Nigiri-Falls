from django.urls import path

from . import views

urlpatterns = [
    path('', views.message_view, name='message'),
    path('list/', views.messagelist_view, name='messagelist')
]
