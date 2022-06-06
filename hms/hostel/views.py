from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import customer,complain,rooms,customer_fee,message
from django.core import mail
from .forms import ImageForm
from datetime import timedelta, date
import stripe
from django.conf import settings
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
                today = date.today()
                print(today)
                EndDate = date.today() + timedelta(days=30)
                room_details = rooms.objects.get(room_id=room)
                new_user=customer(user_name=user_name,email=email,password=password,contact=contact,gender=gender,room=room_details,)
                new_user.save()
                user_data = customer.objects.get(email=email, password=password)
                fee=customer_fee(customer_id=user_data,start_date=today,end_Date=EndDate,total_amount=room_details.room_price)
                fee.save()
                room_current_space=room_details.current_capacity
                room_details.current_capacity=room_current_space+1
                room_details.save()
                messages.success(request,"You are successfully Registered Now")
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
            try:
                data.user_image = form["user_image"]
                data.save()
            except:
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
            data = self.get_data(request.session['id'])
            return render(request, 'room.html',data)
        else:
            return redirect('Login')

    def change_room(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            room_no = request.POST.get('room_no')
            subject = request.POST.get('subject')
            reason_for_change = request.POST.get('reason_for_change')
            student_id = request.session['id']
            register = complain(student_id=student_id, subject=subject, detail=reason_for_change)
            register.save()
            self.send_email("Your complain is registered",
                            "Your complain is registered our representative will contact you soon ", email)
            body = f"subject: {subject} \nUser name: {name} \nUser email: {email} \n Details: {reason_for_change}"
            self.send_email("New complain registered for room change", body, "faisalrasheed442@gmail.com")
            messages.success(request, 'You complaint has been registered')

            return redirect('change_room')

        else:
            if 'id' in request.session:
                data = self.get_data(request.session['id'])
                data["head"] = "Change Room"
                print(data)
                return render(request, 'change_room.html', data)
            else:
                return redirect('Login')



    def complains(self,request):
        # return render(request, 'complains.html')
        if 'id' in request.session:
            data = self.get_data(request.session['id'])
            tickets=complain.objects.filter(customer_id=request.session['id'])
            data['tickets']=tickets
            print(tickets)
            return render(request, 'complains.html',data)
        else:
            return redirect('Login')

    def ticket(self,request):
        if request.method == 'POST':
            subject = request.POST.get('subject')
            reason_for_change = request.POST.get('reason_for_change')
            customer_id = request.session['id']
            user=customer.objects.get(user_id=customer_id)
            new_complain=complain(customer_id=user,subject=subject,detail=reason_for_change)
            new_complain.save()
            return redirect('complains')

        else:
            if 'id' in request.session:
                data = self.get_data(request.session['id'])
                return render(request, 'ticket.html',data)
            else:
                return redirect('Login')
        return render(request,'ticket.html')

    def basic(self,request):
        return render(request,'basic.html')


    def chat(self,request):
        # return render(request, 'fee.html')

        if 'id' in request.session:
            if request.method == "POST":
                data = self.get_data(request.session['id'])
                complain_id=request.POST.get('ticket_id')
                complain_details=complain.objects.get(complian_id=complain_id)
                data["complain"]=complain_details
                data["messages"]=message.objects.filter(complain_id=complain_details)
                try:
                    msg=request.POST.get("msg")
                    new_msg=message(complain_id=complain_details,message=msg,reply="True")
                    new_msg.save()
                except:
                    pass
            return render(request, 'chat.html',data)
        else:
            return redirect('Login')


    def fee_detail(self,request):
        if 'id' in request.session:
            if request.method == 'POST':
                fee_id=request.POST.get("fee_id")
                installment = int(request.POST.get("installment"))
                user=customer.objects.get(user_id=request.session['id'])
                fee=customer_fee.objects.get(fee_id=fee_id)
                end_date=fee.end_Date
                amount=fee.total_amount
                if installment==2:
                    amount=int(amount)/2
                    fee.total_amount=amount
                    fee.end_Date=end_date-timedelta(days=15)
                    fee.allow_installment=False
                    fee.save()
                    new=customer_fee(customer_id=user,start_date=end_date-timedelta(days=15),end_Date=end_date,total_amount=amount,allow_installment=False)
                    new.save()
                elif installment==3:
                    amount = int(amount) / 3
                    fee.total_amount = amount
                    fee.end_Date = end_date - timedelta(days=20)
                    fee.allow_installment = False
                    fee.save()
                    new = customer_fee(customer_id=user, start_date=end_date - timedelta(days=20), end_Date=end_date- timedelta(days=10),
                                       total_amount=amount, allow_installment=False)
                    new.save()
                    new = customer_fee(customer_id=user, start_date=end_date - timedelta(days=10),
                                       end_Date=end_date,
                                       total_amount=amount, allow_installment=False)
                    new.save()
            data = self.get_data(request.session['id'])
            fee_data=customer_fee.objects.filter(customer_id=request.session['id'])
            data['fee']=fee_data
            return render(request, 'fee_detail.html',data)
        else:
            return redirect('Login')
        

    def installment(self,request):
        if request.method == 'POST':
            print("no")
            fee_id = request.POST.get("fee_id")
            fee_data=customer_fee.objects.get(fee_id=fee_id)
            data = self.get_data(request.session['id'])
            data['data']=fee_data
            return render(request, 'installment.html',data)
        else:
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
    def pay_fee(self,request):
        if request.method == 'POST':
            id=request.POST.get("fee_id")
            data=customer_fee.objects.get(fee_id=id)
            price=data.total_amount
            price=price*100
            stripe.api_key=settings.STRIPE_SECRET_KEY
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data':{
                                'currency':'pkr',
                                'unit_amount':price,
                                'product_data':{
                                    'name':"Hostel Fee",
                                },
                            },
                            'quantity':1,
                        },
                    ],
                    mode='payment',
                    success_url= 'http://127.0.0.1:8000/fee/',
                    cancel_url='http://127.0.0.1:8000/fee/',
                )
                data.paid=True
                data.allow_installment=False
                data.save()
            except Exception as e:
                return str(e)
            return redirect(checkout_session.url, code=303)
        else:
            print("yo")
            return redirect("fee")
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




    def send_email(self,subject,text,to):
        connection = mail.get_connection()
        connection.open()
        email1 = mail.EmailMessage(subject,text,"faisalrasheed822@gmail.com",[to],connection=connection,)
        email1.send()
        connection.close()




class admin_view():

    def admin_basic(self,request):
        return render(request,'admin/admin-basic.html')

    def admin_dashboard(self,request):
        return render(request,'admin/admin-dashboard.html')

    def admin_profile(self,request):
        return render(request,'admin/admin-profile.html')

    def admin_update_password(self,request):
        return render(request,'admin/admin-update-password.html')

    def student_registration(self,request):
        return render(request,'admin/student-registration.html')

    def manage_student(self,request):
        return render(request,'admin/manage-student.html')

    def add_room(self,request):
        return render(request,'admin/add-room.html')

    def manage_room(self,request):
        return render(request,'admin/manage-room.html')

    def admin_login(self,request):
        return render(request,'admin/admin-login.html')

    def admin_registration(self,request):
        return render(request,'admin/admin-registration.html')

    def admin_message(self,request):
        return render(request,'admin/admin-message.html')

    def admin_complain(self,request):
        return render(request,'admin/admin-complain.html')
