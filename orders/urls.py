from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_form, name='order_form'),
    path('success/<int:pk>/', views.order_success, name='order_success'),
]
