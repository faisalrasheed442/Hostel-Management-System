from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import customer
import stripe
class student_view():
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
                data=self.get_data(request.session['email'],request.session['password'])
                print(data['profile'].Guardian_name)
                return render(request, 'dashboard.html',data)
            else:
                messages.error(request,'Invalid email and password')
                return redirect('Login')
        else:
            return render(request, 'login.html')

    def register(self,request):
        # return render(request, 'register.html')
        stripe.api_key ='pk_test_51KxEWVGdFjCEtQwCJO7cBduPcL51qqfYWqN3gs5BHWhKx7hoSNkkOEszFJp78zFO1ufDziXM5XVncUI5m5utK6Sf00SXncPGiJ'

        def create_checkout_session():
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'T-shirt',
                        },
                        'unit_amount': 2000,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
            )

            return redirect(session.url, code=303)

    def dashboard(self,request,data={}):
        if 'email' in request.session and 'password' in request.session:
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
        user_data = customer.objects.filter(email=email, password=password)
        user_data = {'profile': user_data[0]}
        return user_data

