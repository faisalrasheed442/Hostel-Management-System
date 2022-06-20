from datetime import timedelta, date

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.core import mail
from django.shortcuts import render, HttpResponse, redirect

from .forms import ImageForm
from .models import customer, complain, rooms, customer_fee, message

# we have created the classs for student view where we will show all the pages that will be shown in student dashboard
# also all the handling for student dashboard is done there
# also we have used if 'id' in session to validate weather the user is logged in or not if not he wont be able to access any page
class student_view():
    # will return the home page of user
    def index(self, request):
        return render(request, 'index.html')

    # login function to authenticate user basically used seasons
    def login(self, request):
        # return render(request,'login.html')
        if 'id' in request.session:
            return redirect('Dashboard')
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                # checking user data to validate
                user_data = customer.objects.get(email=email, password=password)
                request.session['id'] = user_data.user_id
                return redirect('Dashboard')
            except customer.DoesNotExist:
                # email is wrong or password
                messages.error(request, 'Invalid email and password')
                request.session.flush()
                return redirect('Login')
        else:
            return render(request, 'login.html')
    # function to get user register in database getting al the value from form submission
    def register(self, request):
        if request.method == "POST":
            user_name = request.POST.get("user_name")
            email = request.POST.get("email")
            contact = request.POST.get("contact")
            gender = request.POST.get("gender")
            room = request.POST.get("room")
            password = request.POST.get("password")
            food_status = request.POST.get("foodstatus")
            check_email = customer.objects.filter(email=email)
            # checking if the eamils is already registered or not
            if check_email:
                messages.error(request, 'Email Already Registered')
                return redirect('register')
            else:
                # if not user then will create the object for that user
                today = date.today()
                EndDate = date.today() + timedelta(days=30)
                room_details = rooms.objects.get(room_id=room)
                new_user = customer(user_name=user_name, email=email, password=password, contact=contact, gender=gender,
                                    room=room_details, )
                new_user.save()
                user_data = customer.objects.get(email=email, password=password)
                # generating fee for new user
                fee = customer_fee(customer_id=user_data, start_date=today, end_Date=EndDate,
                                   total_amount=room_details.room_price)
                fee.save()
                # updating room details for new uer
                room_current_space = room_details.current_capacity
                room_details.current_capacity = room_current_space + 1
                room_details.save()
                messages.success(request, "You are successfully Registered Now")
                return redirect('register')
        else:
            if 'id' in request.session:
                return redirect('Dashboard')
            else:
                data = rooms.objects.filter(current_capacity__lt=5)
                data = {'room': data}
                print(data)
                return render(request, 'register.html', data)
    # display user dashboard
    def dashboard(self, request):
        # return render(request,'dashboard.html')
        if 'id' in request.session:
            data = self.get_data(request.session['id'])
            return render(request, 'dashboard.html', data)
        else:
            return redirect('Login')
    # will update user data in profile and show his information
    def profile(self, request):
        form = ImageForm()
        if request.method == 'POST':
            form = request.FILES
            username = request.POST.get('name')
            contact = request.POST.get('contact')
            gender = request.POST.get('gender')
            guardian_name = request.POST.get('guardian_name')
            guardian_contact = request.POST.get('guardian_contact')
            address = request.POST.get('address')
            data = customer.objects.get(user_id=request.session['id'])
            data.user_name = username
            data.gender = gender
            data.Guardian_contact = guardian_contact
            data.Guardian_name = guardian_name
            data.contact = contact
            data.address = address
            # updating user information
            try:
                # ifuser has uploaded an image the try will save the image
                data.user_image = form["user_image"]
                data.save()
            except:
                # if user hasnot uploaded image the try will through error and will go to expect
                # and save remaing data
                data.save()
            return redirect('profile')
        if 'id' in request.session:
            data = self.get_data(request.session['id'])
            data["form"] = form
            return render(request, 'profile.html', data)
        else:
            return redirect('Login')
    # showing user room detail
    def room(self, request):
        # return render(request, 'room.html')
        if 'id' in request.session:
            data = self.get_data(request.session['id'])
            return render(request, 'room.html', data)
        else:
            return redirect('Login')
    # will send request if youser want to change room
    def change_room(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            room_no = request.POST.get('room_no')
            subject = request.POST.get('subject')
            reason_for_change = request.POST.get('reason_for_change')
            student_id = request.session['id']
            user = customer.objects.get(user_id=student_id)
            register = complain(customer_id=user, subject=subject, detail=reason_for_change)
            register.save()
            # sending email to both admin and user for new complain
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

    def complains(self, request):
        # showinf all the complains for user
        if 'id' in request.session:
            data = self.get_data(request.session['id'])
            tickets = complain.objects.filter(customer_id=request.session['id'])
            data['tickets'] = tickets
            return render(request, 'complains.html', data)
        else:
            return redirect('Login')
    # create new complain for the problem
    def ticket(self, request):
        if request.method == 'POST':
            subject = request.POST.get('subject')
            reason_for_change = request.POST.get('reason_for_change')
            customer_id = request.session['id']
            user = customer.objects.get(user_id=customer_id)
            new_complain = complain(customer_id=user, subject=subject, detail=reason_for_change)
            new_complain.save()
            return redirect('complains')

        else:
            if 'id' in request.session:
                data = self.get_data(request.session['id'])
                return render(request, 'ticket.html', data)
            else:
                return redirect('Login')
        return render(request, 'ticket.html')

    def basic(self, request):
        return render(request, 'basic.html')
    # showing all the chat for a particulare ticket
    def chat(self, request):
        # return render(request, 'fee.html')

        if 'id' in request.session:
            if request.method == "POST":
                data = self.get_data(request.session['id'])
                complain_id = request.POST.get('ticket_id')
                complain_details = complain.objects.get(complian_id=complain_id)
                data["complain"] = complain_details
                data["messages"] = message.objects.filter(complain_id=complain_details)
                try:
                    msg = request.POST.get("msg")
                    new_msg = message(complain_id=complain_details, message=msg, reply="True")
                    new_msg.save()
                except:
                    pass
            return render(request, 'chat.html', data)
        else:
            return redirect('Login')
    # showing all the ffes that user has to pay
    def fee_detail(self, request):
        if 'id' in request.session:
            if request.method == 'POST':
                fee_id = request.POST.get("fee_id")
                installment = int(request.POST.get("installment"))
                user = customer.objects.get(user_id=request.session['id'])
                fee = customer_fee.objects.get(fee_id=fee_id)
                end_date = fee.end_Date
                amount = fee.total_amount
                if installment == 2:
                    amount = int(amount) / 2
                    fee.total_amount = amount
                    fee.end_Date = end_date - timedelta(days=15)
                    fee.allow_installment = False
                    fee.save()
                    new = customer_fee(customer_id=user, start_date=end_date - timedelta(days=15), end_Date=end_date,
                                       total_amount=amount, allow_installment=False)
                    new.save()
                elif installment == 3:
                    amount = int(amount) / 3
                    fee.total_amount = amount
                    fee.end_Date = end_date - timedelta(days=20)
                    fee.allow_installment = False
                    fee.save()
                    new = customer_fee(customer_id=user, start_date=end_date - timedelta(days=20),
                                       end_Date=end_date - timedelta(days=10),
                                       total_amount=amount, allow_installment=False)
                    new.save()
                    new = customer_fee(customer_id=user, start_date=end_date - timedelta(days=10),
                                       end_Date=end_date,
                                       total_amount=amount, allow_installment=False)
                    new.save()
            data = self.get_data(request.session['id'])
            fee_data = customer_fee.objects.filter(customer_id=request.session['id'])
            data['fee'] = fee_data
            return render(request, 'fee_detail.html', data)
        else:
            return redirect('Login')
    # if the user want to create installment for fee
    def installment(self, request):
        if request.method == 'POST':
            print("no")
            fee_id = request.POST.get("fee_id")
            fee_data = customer_fee.objects.get(fee_id=fee_id)
            data = self.get_data(request.session['id'])
            data['data'] = fee_data
            return render(request, 'installment.html', data)
        else:
            return render(request, 'installment.html')

    def passwords(self, request):
        # return render(request,'password.html')
        if request.method == 'POST':
            print("hire")
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            cpassword = request.POST.get('cpassword')
            print(cpassword)
            user_data = self.get_data(request.session['id'])
            if oldpassword == user_data['profile'].password and newpassword == cpassword:
                update = customer.objects.get(user_id=request.session['id'])
                update.password = newpassword
                update.save()
                messages.success(request, "Password changed")
                return redirect("password")
            else:
                messages.error(request, "some details are wrong")
                return redirect("password")

        else:
            if 'id' in request.session:
                data = self.get_data(request.session['id'])
                return render(request, 'password.html',data)
            else:
                return redirect('Login')

    def pay_fee(self, request):
        if request.method == 'POST':
            id = request.POST.get("fee_id")
            data = customer_fee.objects.get(fee_id=id)
            price = data.total_amount
            price = price * 100
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'pkr',
                                'unit_amount': price,
                                'product_data': {
                                    'name': "Hostel Fee",
                                },
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url='http://127.0.0.1:8000/fee/',
                    cancel_url='http://127.0.0.1:8000/fee/',
                )
                data.paid = True
                data.allow_installment = False
                data.save()
            except Exception as e:
                return str(e)
            return redirect(checkout_session.url, code=303)
        else:
            print("yo")
            return redirect("fee")

    def logout(self, request):
        # return render(request, 'logout.html')
        if 'id' in request.session:
            request.session.flush()
            return redirect('Login')
        else:
            return redirect('Login')

    # Forget Password
    def forget_password(self, request):
        return render(request, 'forget_password.html')

    def get_data(self, id):
        user_data = customer.objects.get(user_id=id)
        user_data = {'profile': user_data}
        return user_data

    def send_email(self, subject, text, to):
        connection = mail.get_connection()
        connection.open()
        email1 = mail.EmailMessage(subject, text, "faisalrasheed822@gmail.com", [to], connection=connection, )
        email1.send()
        connection.close()



# Admin Data
class admin_view():
    def admin_basic(self, request):
        return render(request, 'admin/admin-basic.html')

    def admin_login(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("admin-dashboard")
            else:
                messages.error(request, 'Invalid email and password')
                return redirect('admin-login')
        if request.user.is_authenticated:
            return render(request, 'admin/admin-dashboard.html')
        else:

            return render(request, 'admin/admin-login.html')

    def admin_dashboard(self, request):
        if request.user.is_authenticated:
            return render(request, 'admin/admin-dashboard.html')
        else:
            return redirect('admin-login')

    def admin_profile(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('user_name')
                request.user.username = username
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()
                messages.success(request, "Profile Updated")
                return redirect('admin-profile')
            else:
                return render(request, 'admin/admin-profile.html', {"data": request.user})
        else:
            return redirect('admin-login')

    def admin_update_password(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                old_password = request.POST.get('oldpassword')
                match = check_password(old_password, request.user.password)
                new_password = request.POST.get("newpassword")
                confirm_password = request.POST.get("cpassword")
                print(request.user.password)
                if match and new_password == confirm_password:
                    request.user.password = new_password
                    request.user.save()
                    messages.success(request, "Password Updated")
                else:
                    messages.error(request, "Some details are wrong")
                return redirect("admin-update-password")
            else:
                print(request.user.password)
                return render(request, 'admin/admin-update-password.html')
        else:
            return redirect('admin-login')

    def student_registration(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                user_name = request.POST.get("user_name")
                email = request.POST.get("email")
                contact = request.POST.get("contact")
                gender = request.POST.get("gender")
                room = request.POST.get("room")
                password = request.POST.get("password")
                feestatus = request.POST.get("feestatus")
                installment = True
                if feestatus == "True":
                    installment = False
                check_email = customer.objects.filter(email=email)
                if check_email:
                    messages.error(request, 'Email Already Registered')
                    return redirect('student-registration')
                else:
                    today = date.today()
                    EndDate = date.today() + timedelta(days=30)
                    room_details = rooms.objects.get(room_id=room)
                    new_user = customer(user_name=user_name, email=email, password=password, contact=contact,
                                        gender=gender, room=room_details, )
                    new_user.save()
                    user_data = customer.objects.get(email=email, password=password)
                    fee = customer_fee(customer_id=user_data, start_date=today, end_Date=EndDate,
                                       total_amount=room_details.room_price, paid=feestatus,
                                       allow_installment=installment)
                    fee.save()
                    room_current_space = room_details.current_capacity
                    room_details.current_capacity = room_current_space + 1
                    room_details.save()
                    messages.success(request, "You are successfully Registered Now")
                    return redirect('student-registration')
            else:
                data = rooms.objects.filter(current_capacity__lt=5)
                data = {'room': data}
                return render(request, 'admin/student-registration.html', data)
        else:
            return redirect('admin-login')

    def manage_student(self, request):
        if request.user.is_authenticated:
            user = customer.objects.all()
            return render(request, 'admin/manage-student.html', {"users": user})
        else:
            return redirect('admin-login')

    def update_student(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                if 'send_update' in request.POST:
                    user_id = request.POST.get("user_id")
                    request.session["current_update"] = user_id
                elif 'update' in request.POST:
                    user_id = request.session["current_update"]
                    data = customer.objects.get(user_id=user_id)
                    name = request.POST.get('name')
                    email = request.POST.get('email')
                    contact = request.POST.get('contact')
                    room_id = request.POST.get('room')
                    gender = request.POST.get("gender")
                    data.user_name = name
                    data.email = email
                    data.gender = gender
                    data.contact = contact
                    data.save()
                    messages.success(request, "User is updated successfully")
                    if int(room_id) == data.room.room_id:
                        pass
                    else:
                        room = rooms.objects.get(room_id=data.room.room_id)
                        room.current_capacity -= 1
                        room.save()
                        room = rooms.objects.get(room_id=room_id)
                        data.room = room
                        data.save()
                        room.current_capacity += 1
                        room.save()

                user = customer.objects.get(user_id=user_id)
                room = rooms.objects.filter(current_capacity__lt=5)
                return render(request, 'admin/update-student.html', {"profile": user, 'room': room})
        else:
            return redirect('admin-login')

    def add_room(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                room_capacity = request.POST.get("capacity")
                name = request.POST.get("name")
                price = request.POST.get("fee")
                room = rooms(room_name=name, room_capacity=room_capacity, room_price=price)
                room.save()
                messages.success(request, "New Room added")
            return render(request, 'admin/add-room.html')
        else:
            return redirect('admin-login')

    def manage_room(self, request):
        if request.user.is_authenticated:
            room = rooms.objects.all()
            return render(request, 'admin/manage-room.html', {"rooms": room})
        else:
            return redirect('admin-login')

    def update_room(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                room_id = request.POST.get("room_id")
                room_data = rooms.objects.get(room_id=room_id)
                if 'delete' in request.POST:
                    room_data.delete()
                    return redirect("manage-room")
                elif 'update' in request.POST:
                    capacity = request.POST.get("seater")
                    name = request.POST.get("name")
                    price = request.POST.get("price")
                    current_capacity = request.POST.get("current_capacity")
                    room_data.room_capacity = capacity
                    room_data.room_name = name
                    room_data.room_price = price
                    room_data.current_capacity = current_capacity
                    room_data.save()
                    messages.success(request, "Room details are Updated")

                return render(request, 'admin/update-room.html', {"room": room_data})
        else:
            return redirect('admin-login')

    def admin_message(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                to = request.POST.get("email")
                subject = request.POST.get("subject")
                print(to)
                body = request.POST.get("body")
                self.send_email(subject,
                                body, to)
                messages.success(request, "Email is send")
            return render(request, 'admin/admin-message.html')
        else:
            return redirect('admin-login')

    def send_email(self, subject, text, to):
        connection = mail.get_connection()
        connection.open()
        email1 = mail.EmailMessage(subject, text, "shirazsweer12@pepisandbox.com", [to], connection=connection, )
        email1.send()
        connection.close()

    def admin_complain(self, request):
        if request.user.is_authenticated:
            ticket = complain.objects.all()
            return render(request, 'admin/admin-complain.html', {"tickets": ticket})
        else:
            return redirect('admin-login')

    def chat_now(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                data = {}
                complain_id = request.POST.get('ticket_id')
                complain_details = complain.objects.get(complian_id=complain_id)
                # customer_id=complain.customer_id
                # print(customer_id)
                data["complain"] = complain_details
                data["messages"] = message.objects.filter(complain_id=complain_details)
                try:
                    msg = request.POST.get("msg")
                    new_msg = message(complain_id=complain_details, message=msg, reply="False")
                    new_msg.save()
                except:
                    pass
            return render(request, 'admin/chat-now.html', data)
        else:
            return redirect('admin-login')

    def chat_resolved(self, request):
        if request.method == "POST":
            id = request.POST.get("ticket_id")
            data_of_complain = complain.objects.get(complian_id=id)
            data_of_complain.complain_status = True
            data_of_complain.save()
            return redirect('admin-complain')

    def fee_detail(self, request):
        if request.user.is_authenticated:
            data = customer_fee.objects.all()

            return render(request, 'admin/fee-details.html', {"fees": data})
        else:
            return redirect('admin-login')

    def payfee(self, request):
        if request.method == "POST":
            fee_id = request.POST.get('id')
            fee = customer_fee.objects.get(fee_id=fee_id)
            fee.paid = True
            fee.allow_installment = False
            fee.save()
            return redirect('fee-detail')

    def admin_logout(self, request):
        logout(request)
        return redirect('admin-login')
