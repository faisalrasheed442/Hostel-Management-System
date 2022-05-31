from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import customer,complain
from django.core import mail
# import stripe

class student_view():
    def index(self,request):
        return render(request, 'index.html')
    # login function to authenticate user basically used seassons


    def login(self,request):
        # return render(request,'login.html')
        if 'id' in request.session:
            return redirect('Dashboard')
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user_data= customer.objects.get(email=email,password=password)
                request.session['id'] = user_data.user_id
                return redirect('Dashboard')
            except customer.DoesNotExist:
                messages.error(request, 'Invalid email and password')
                request.session.flush()
                return redirect('Login')
        else:
            return render(request, 'login.html')


    def register(self,request):
        # return render(request, 'register.html')
        if 'id' in request.session:
            return redirect('Dashboard')
        else:
            return render(request, 'register.html')


    def dashboard(self,request):
        # return render(request,'dashboard.html')
        if 'id' in request.session:
            data=self.get_data(request.session['id'])
            return render(request, 'dashboard.html',data)
        else:
            return redirect('Login')


    def profile(self,request):
        # return render(request, 'profile.html')
        if request.method == 'POST':
            username=request.POST.get('name')
            contact=request.POST.get('contact')
            gender=request.POST.get('gender')
            guardian_name=request.POST.get('guardian_name')
            guardian_contact=request.POST.get('guardian_contact')
            address=request.POST.get('address')
            data=customer.objects.get(user_id=request.session['id'])
            data.user_name=username
            data.gender=gender
            data.Guardian_contact=guardian_contact
            data.Guardian_name=guardian_name
            data.contact=contact
            data.address=address
            data.save()
            return redirect('profile')
        if 'id' in request.session:
            data = self.get_data(request.session['id'])
            return render(request, 'profile.html',data)
        else:
            return redirect('Login')


    def room(self,request):
        # return render(request, 'room.html')
        if 'id' in request.session:
            return render(request, 'room.html')
        else:
            return redirect('Login')

    def book_room(self,request):
        return render(request, 'book_room.html')


    def complains(self,request):
        # return render(request, 'complains.html')
        if 'id' in request.session:
            return render(request, 'complains.html')
        else:
            return redirect('Login')

    def ticket(self,request):
        return render(request,'ticket.html')

    def basic(self,request):
        return render(request,'basic.html')


    def fee(self,request):
        # return render(request, 'fee.html')

        if 'id' in request.session:
            return render(request, 'fee.html')
        else:
            return redirect('Login')


    def fee_detail(self,request):
        return render(request,'fee_detail.html')


    def passwords(self,request):
        # return render(request,'password.html')
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
        # return render(request, 'logout.html')
        if 'id' in request.session:
            request.session.flush()
            return redirect('Login')
        else:
            return redirect('Login')

    # Forget Password
    def forget_password(self,request):
        return render(request,'forget_password.html')

    def get_data(self,id):
        user_data = customer.objects.get(user_id=id)
        user_data = {'profile': user_data}
        return user_data

    def change_room(self,request):
        # return render(request, 'change_room.html')
        if request.method == 'POST':
            name=request.POST.get('name')
            email=request.POST.get('email')
            contact=request.POST.get('contact')
            room_no=request.POST.get('room_no')
            subject=request.POST.get('subject')
            reason_for_change=request.POST.get('reason_for_change')
            student_id = request.session['id']
            register = complain(student_id=student_id, subject=subject, detail=reason_for_change)
            register.save()
            self.send_email("Your complain is registered","Your complain is registered our representative will contact you soon ",email)
            body=f"subject: {subject} \nUser name: {name} \nUser email: {email} \n Details: {reason_for_change}"
            self.send_email("New complain registered for room change",body,"faisalrasheed442@gmail.com")
            messages.success(request, 'You complaint has been registered')
        
            return redirect('change_room')
        
        else:
            if 'id' in request.session:
                data=self.get_data(request.session['id'])
                return render(request, 'change_room.html',data)
            else:
                return redirect('Login')


    def send_email(self,subject,text,to):
        connection = mail.get_connection()
        connection.open()
        email1 = mail.EmailMessage(subject,text,"faisalrasheed822@gmail.com",[to],connection=connection,)
        email1.send()
        connection.close()



