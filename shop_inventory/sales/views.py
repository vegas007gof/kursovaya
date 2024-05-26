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

    products = Product.objects.all()
    sales_summary = Sale.objects.values('product__name').annotate(total_quantity_sold=Sum('quantity_sold')).order_by(
        'product__name')
    total_sales = sales.aggregate(total_quantity_sold=Sum('quantity_sold'))['total_quantity_sold'] or 0
    total_revenue = sales.aggregate(total_revenue=Sum('product__price'))['total_revenue'] or 0

    return render(request, 'sales/sales_report.html', {
        'sales': sales,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'start_date': start_date,
        'end_date': end_date,
        'products': products,
        'sales_summary': sales_summary,
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
