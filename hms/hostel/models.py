from django.db import models
import time
# Create your models here.
class rooms(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name=models.CharField(max_length=30)
    room_capacity=models.IntegerField(default=5)
    room_price=models.IntegerField(default=6000)

    def __str__(self):
        return self.room_name
class complain(models.Model):
    complian_id=models.AutoField(primary_key=True)
    student_id = models.IntegerField()
    subject=models.CharField(max_length=100)
    detail=models.CharField(max_length=500)
    complain_status=models.BooleanField(default=False)


    def __str__(self):
        return self.subject

class customer(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=30)
    contact=models.CharField(max_length=20,default="")
    room=models.ForeignKey(rooms,on_delete=models.CASCADE)
    gender=models.CharField(max_length=30,default='Not Mentioned')
    Guardian_name=models.CharField(max_length=100)
    Guardian_contact=models.CharField(max_length=20)
    payment_staus=models.BooleanField()
    registration_date=models.DateField()
    user_image=models.ImageField(upload_to="static/profile_image",default="static/profile_image/avatar1.png")
    address=models.CharField(max_length=500)
    food_status=models.BooleanField(default=False)


    def __str__(self):
        return self.user_name
class customer_fee(models.Model):
    fee_id=models.ForeignKey(customer,on_delete=models.CASCADE)
    start_date=models.DateTimeField()
    end_Date=models.DateField()
    total_amount=models.IntegerField()
    allow_installment=models.BooleanField(default=True)





