from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AdminSignUpForm, SalesExecutiveSignUpForm, InventoryManagerSignUpForm
from django.contrib.auth import login, logout, authenticate 
from .models import CustomUser


# Create your views here.

def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Admin account created successfully.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AdminSignUpForm()
    
    return render(request, 'accounts/signup.html', {'form_data': form,'user_type': 'Admin'})


def sales_executive_signup(request):
    if request.method == 'POSt':
        form = SalesExecutiveSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Sales Executive account created successfully.")
            return redirect('sales_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SalesExecutiveSignUpForm()
    
    return render(request, 'accounts/signup.html', {'form_data': form,'user_type': 'Sales Executive'})


def inventory_manager_signup(request):
    if request.method == 'POST':
        form = InventoryManagerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inventory Manager account created successfully.")
            return redirect('inventory_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InventoryManagerSignUpForm()
    return render(request, 'accounts/signup.html', {'form_data': form,'user_type': 'Inventory Manager'})


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user_obj.email, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            
            if user.roles == 'admin':
                messages.success(request, "Logged in successfully as Admin.")
                return redirect('admin_dashboard')
            elif user.roles == 'sales':
                messages.success(request, "Logged in successfully as Sales Executive.")
                return redirect('sales_dashboard')
            elif user.roles == 'inventory':
                messages.success(request, "Logged in successfully as Inventory Manager.")
                return redirect('inventory_dashboard')
            else:
                messages.error(request, "Invalid user role.")
                logout(request)

    return render(request, 'accounts/login.html')


