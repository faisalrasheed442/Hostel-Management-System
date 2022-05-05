from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import customer
class student_view():
    def __init__(self):
        self.data={}
    def index(self,request):
        return render(request, 'index.html')

    def login(self,request):
        if 'email' in request.session and 'password' in request.session:
            return self.dashboard(request, self.data)

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_data=customer.objects.filter(email=email,password=password)
            if user_data:
                request.session['email'] = email
                request.session['password'] = password
                user_data={'profile':user_data[0]}
                self.data=user_data
                print(self.data['profile'].contact)
                return render(request, 'dashboard.html',self.data)
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
        if 'email' in request.session and 'password' in request.session:
            return render(request, 'profile.html',self.data)
        else:
            return redirect('Login')


    def room(self,request):
        if 'email' in request.session and 'password' in request.session:
            return render(request, 'room.html')
        else:
            return redirect('Login')


    def complains(self,request):
        if 'email' in request.session and 'password' in request.session:
            return render(request, 'complains.html')
        else:
            return redirect('Login')


    def fee(self,request):
        if 'email' in request.session and 'password' in request.session:
            return render(request, 'fee.html')
        else:
            return redirect('Login')


    def passwords(self,request):
        if 'email' in request.session and 'password' in request.session:
            return render(request, 'password.html')
        else:
            return redirect('Login')

    def logout(self,request):
        if 'email' in request.session and 'password' in request.session:
            request.session.flush()
            return redirect('Login')
        else:
            return redirect('Login')
