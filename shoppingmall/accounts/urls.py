from django.urls import path
from . import views

urlpatterns = [
    path('signup/buyer', views.buyersignup, name='buyersignup'),
    path('signup/seller', views.sellersignup, name='sellersignup'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
