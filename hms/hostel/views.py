from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import customer
class student_view():
    def __init__(self):
        self.password=None
        self.email=None
        self.data={}
    def index(self,request):
        return render(request, 'index.html')

    def login(self,request):
        if self.email and self.password:
            return self.dashboard(request, self.data)

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_data=customer.objects.filter(email=email,password=password)
            if user_data:
                user_data={'profile':user_data[0]}
                self.email = email
                self.password=password
                self.data=user_data
                print(self.data['profile'].contact)
                return self.dashboard(request,self.data)
            else:
                messages.error(request,'Invalid email and password')
                return redirect('Login')
        else:
            return render(request, 'login.html')

    def register(self,request):
        return render(request, 'register.html')

    def dashboard(self,request,data={}):
        return render(request, 'dashboard.html',data)

    def profile(self,request):
        if self.email and self.password:
            return render(request, 'profile.html',self.data)

    def room(self,request):
        return render(request, 'room.html')

    def complains(self,request):
        return render(request, 'complains.html')

    def fee(self,request):
        return render(request, 'fee.html')

    def passwords(self,request):
        return render(request, 'password.html')
    def logout(self,request):
        if self.email and self.password:
            self.email=None
            self.password=None
            self.data={}
            return redirect('Login')
        else:
            return redirect('Login')
