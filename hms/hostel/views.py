from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import customer,complain,rooms,customer_fee
from django.core import mail
from .forms import ImageForm
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
        if request.method=="POST":
            user_name=request.POST.get("user_name")
            print(user_name)
            email=request.POST.get("email")
            contact=request.POST.get("contact")
            gender=request.POST.get("gender")
            room=request.POST.get("room")
            password=request.POST.get("password")
            food_status=request.POST.get("foodstatus")
            check_email=customer.objects.filter(email=email)
            if check_email:
                messages.error(request, 'Email Already Registered')
                return redirect('register')
            else:
                new_user=customer(user_name=user_name,email=email,password=password,contact=contact,gender=gender,room=room,)
                return redirect('register')
        else:
            if 'id' in request.session:
                return redirect('Dashboard')
            else:
                data=rooms.objects.filter(current_capacity__lt=5)
                data={'room':data}
                print(data)
                return render(request, 'register.html',data)


    def dashboard(self,request):
        # return render(request,'dashboard.html')
        if 'id' in request.session:
            data=self.get_data(request.session['id'])
            return render(request, 'dashboard.html',data)
        else:
            return redirect('Login')


    def profile(self,request):
        form=ImageForm()
        if request.method == 'POST':
            form=request.FILES
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
            data.user_image=form["user_image"]
            data.save()
            return redirect('profile')
        if 'id' in request.session:
            data = self.get_data(request.session['id'])
            data["form"] = form
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


    def chat(self,request):
        # return render(request, 'fee.html')

        if 'id' in request.session:
            return render(request, 'chat.html')
        else:
            return redirect('Login')


    def fee_detail(self,request):
        if 'id' in request.session:
            data=customer_fee.objects.filter(customer_id=request.session['id'])
            print(data)
            data={"fee":data}
            return render(request, 'fee_detail.html',data)
        else:
            return redirect('Login')
        

    def installment(self,request):
        if request.method == 'POST':
            print("no")
            fee_id = request.POST.get("fee_id")
            data=customer_fee.objects.get(fee_id=fee_id)
            data={"data":data}
            return render(request, 'installment.html',data)
        else:
            print("error")
            data=request.POST.get("price")
            return render(request, 'installment.html')

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
                data["head"]="Change Room"
                print(data)
                return render(request, 'change_room.html',data)
            else:
                return redirect('Login')


    def send_email(self,subject,text,to):
        connection = mail.get_connection()
        connection.open()
        email1 = mail.EmailMessage(subject,text,"faisalrasheed822@gmail.com",[to],connection=connection,)
        email1.send()
        connection.close()




class admin_view():
    def index(self,request):
        return render(request, 'index.html')
