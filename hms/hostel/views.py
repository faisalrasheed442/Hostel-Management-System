from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import customer
# import stripe
class student_view():
    def index(self,request):
        return render(request, 'index.html')
    # login function to authenticate user basically used seassons
    def login(self,request):
        if 'id' in request.session:
            return redirect('Dashboard')
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_data=user_data = customer.objects.get(email=email,password=password)
            if user_data:
                request.session['id'] =user_data.user_id
                return redirect('Dashboard')
            else:
                messages.error(request,'Invalid email and password')
                request.session.flush()
                return redirect('Login')
        else:
            return render(request, 'login.html')

    def register(self,request):
        if 'email' in request.session and 'password' in request.session:
            return redirect('Dashboard')
        else:
            return render(request, 'register.html')


    def dashboard(self,request):
        if 'id' in request.session:
            data=self.get_data(request.session['id'])
            return render(request, 'dashboard.html',data)
        else:
            return redirect('Login')


    def profile(self,request):
        if 'id' in request.session:
            data = self.get_data(request.session['id'])
            return render(request, 'profile.html',data)
        else:
            return redirect('Login')


    def room(self,request):
        if 'id' in request.session:
            return render(request, 'room.html')
        else:
            return redirect('Login')


    def complains(self,request):
        if 'id' in request.session:
            return render(request, 'complains.html')
        else:
            return redirect('Login')


    def fee(self,request):
        if 'id' in request.session:
            return render(request, 'fee.html')
        else:
            return redirect('Login')


    def passwords(self,request):
        if request.method == 'POST':
            print("hire")
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            cpassword = request.POST.get('cpassword')
            print(cpassword)
            user_data=self.get_data(request.session['id'])
            if oldpassword==user_data['profile'].password and newpassword==cpassword:
                update=customer.objects.get(user_id=request.session['id'])
                update.password=newpassword
                update.save()
                messages.success(request,"Password changed")
                return render(request, 'password.html')
            else:
                messages.error(request,"some details are wrong")
                return render(request, 'password.html')

        else:
            if 'id' in request.session:
                return render(request, 'password.html')
            else:
                return redirect('Login')

    def logout(self,request):
        if 'id' in request.session:
            request.session.flush()
            return redirect('Login')
        else:
            return redirect('Login')
    def get_data(self,id):
        user_data = customer.objects.get(user_id=id)
        user_data = {'profile': user_data}
        return user_data

    def change_room(self,request):
        return render(request, 'change_room.html')


