from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import customer
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_data=customer.objects.filter(email=email,password=password)
        if user_data:
            user_data={'profile':user_data[0]}
            return dashboard(request,user_data)
        else:

            messages.error(request,'Invalid email and password')
            return redirect('Login')
    else:
        return render(request, 'login.html')

def handle_login(request):
    if request.method == 'POST':
        email_login = request.POST['email']
        password_login = request.POST['password']
        user=authenticate(email=email_login,password=password_login)
        if user is not None:
            login(request,user)
            return redirect('Dashboard')
        else:
            messages.error(request,"invalid Logged in")
            return redirect('Home')
def register(request):
    return render(request, 'register.html')

def dashboard(request,data):
    return render(request, 'dashboard.html',data)

def profile(request):
    return render(request, 'profile.html')

def room(request):
    return render(request, 'room.html')

def complains(request):
    return render(request, 'complains.html')

def fee(request):
    return render(request, 'fee.html')

def password(request):
    return render(request, 'password.html')