from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.urls import is_valid_path
from sqlalchemy import null
from .models import *
from .forms import CreateUserForm, OrderForm 
from .filters import OrderFilter 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# Adding message
from django.contrib import messages



# Create your views here.

def registerPage(request):
	form = CreateUserForm()

	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created successfuly for '+ user)
			return redirect('login')
	context = {'form': form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')

	context = {}
	return render(request, 'accounts/login.html', context)

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
	orders = customer.order_set.all()
	orders_total = orders.count()
	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs
	context = {"customer": customer, 'orders': orders, 'orders_total': orders_total, 'myFilter': myFilter}
	return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):

# Creating inline forms
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
	customer = Customer.objects.get(id=pk)
	formSet = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm(initial={'customer': customer})
	if request.method == 'POST':
		# print('Printing POST: ', request.POST)
		# form = OrderForm(request.POST)
		formSet = OrderFormSet(request.POST, instance=customer)
		if formSet.is_valid():
			formSet.save()
			return redirect('/')
	context = {'formSet': formSet}
	return render(request, 'accounts/order_form.html', context)

def updateOrders(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		# print('Printing POST: ', request.POST)
		form = OrderForm(request.POST, instance=order)

		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

def deleteOrders (request, pk):
	order = Order.objects.get(id=pk)

	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'order':order}
	return render(request, 'accounts/delete.html', context)

 