from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    path('', views.index, name='Home'),
    path('login/', views.login, name='Login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='Dashboard'),
    path('profile/', views.profile, name='profile'),
    path('room/', views.room, name='room'),
    path('complains/', views.complains, name='complains'),
    path('fee/', views.fee, name='fee'),
    path('password/', views.password, name='password')

]