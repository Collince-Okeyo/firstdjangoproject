from django.urls import path
from . import views

urlpatterns = [
	path('', views.home),
	path('products/', views.products),
	# Dynamic URL routing
	path('customer/<str:pk_test>/', views.customer)

]