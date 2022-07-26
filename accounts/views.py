from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

# Rendering templates
def home(request):
	# Showing the data in the home
	orders = Order.objects.all()
	customers = Customer.objects.all()

	totoal_customers = customers.count()

# Rendering data to templates
	total_orders = orders.count()
	delivered = orders.filter(status="Delivered").count()
	pending = orders.filter(status="Pending").count()

	context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}

	return render(request, 'accounts/dashboard.html', context)

def products(request):
	products = Product.objects.all()
	# Rendering products to the view using teplates
	return render(request, 'accounts/products.html', {'products':products})

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	return render(request, 'accounts/customer.html')