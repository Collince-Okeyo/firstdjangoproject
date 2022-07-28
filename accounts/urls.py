from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('', views.home, name="home"),
	path('products/', views.products, name="products"),
	# Dynamic URL routing
	path('customer/<str:pk_test>/', views.customer, name="customer"),

	path('create_order/<str:pk>/', views.createOrder, name="create_order"),
	path('update_order/<str:pk>/', views.updateOrders, name="update_order"),
	path('delete_order/<str:pk>/', views.deleteOrders, name="delete_order"),

]