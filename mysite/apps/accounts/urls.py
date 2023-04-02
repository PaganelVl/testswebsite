from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('login/', views.MySiteLoginView.as_view(), name='MySiteLoginView'),
	path('register/', views.RegisterUserView.as_view(), name='RegisterUserView'),
	path('logout/', views.MySiteLogout.as_view(), name='MySiteLogout')
]