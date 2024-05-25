from django.shortcuts import render, redirect
from .models import Product, Sale
from .forms import SaleForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import ProductForm

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_report')
    else:
        form = ProductForm()
    return render(request, 'sales/add_product.html', {'form': form})
def index(request):
    products = Product.objects.all()
    return render(request, 'sales/index.html', {'products': products})

#@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SaleForm()
    return render(request, 'sales/sale_form.html', {'form': form})

#@login_required
def sales_list(request):
    products = Product.objects.all()  # Переменная products
    return render(request, 'sales/sales_list.html', {'products': products})


def sales_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        sales = Sale.objects.filter(date_sold__range=(start_date, end_date))
    else:
        sales = Sale.objects.all()

    total_sales = sales.aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0
    total_revenue = sales.aggregate(Sum('product__price'))['product__price__sum'] or 0

    return render(request, 'sales/sales_report.html', {
        'sales': sales,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'start_date': start_date,
        'end_date': end_date,
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'sales/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request, 'sales/logout.html')
