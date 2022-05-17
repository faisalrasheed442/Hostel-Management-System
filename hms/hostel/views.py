from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import customer
# import stripe
class student_view():
    def index(self,request):
        return render(request, 'index.html')

    def login(self,request):
        if 'email' in request.session and 'password' in request.session:
            return redirect('Dashboard')

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_data=customer.objects.filter(email=email,password=password)
            if user_data:
                request.session['email'] = email
                request.session['password'] = password
                data=self.get_data(request.session['email'],request.session['password'])
                print(data['profile'].Guardian_name)
                return redirect('Dashboard')
            else:
                messages.error(request,'Invalid email and password')
                return redirect('Login')
        else:
            return render(request, 'login.html')

    def register(self,request):
        if 'email' in request.session and 'password' in request.session:
            return redirect('Dashboard')
        else:
            return render(request, 'register.html')


    def dashboard(self,request):
        if 'email' in request.session and 'password' in request.session:
            data=self.get_data(request.session['email'],request.session['password'])
            return render(request, 'dashboard.html',data)
        else:
            return redirect('Login')


    def profile(self,request):
        if 'email' in request.session and 'password' in request.session:
            data = self.get_data(request.session['email'], request.session['password'])
            return render(request, 'profile.html',data)
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
    def get_data(self,email,password):
        user_data = customer.objects.get(email=email, password=password)
        print(user_data.user_image)
        user_data = {'profile': user_data}
        return user_data

    def change_room(self,request):
        return render(request, 'change_room.html')
