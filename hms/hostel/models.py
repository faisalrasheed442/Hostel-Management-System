from django.db import models
from datetime import datetime
# Create your models here.

# this the class we created to store our rooms information
class rooms(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name=models.CharField(max_length=30)
    room_capacity=models.IntegerField(default=5)
    room_price=models.IntegerField(default=6000)
    current_capacity=models.IntegerField(default=0)

    def __str__(self):
        return self.room_name

# Thgis class is for our user whioch can be student or any customer that want to to stay at hostel
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
    user_image=models.ImageField(upload_to="static/profile_image",default="static/profile_image/avatar1.png")
    address=models.CharField(max_length=500)
    food_status=models.BooleanField(default=False)
    stay_from=models.DateField(default=datetime.today)
    def __str__(self):
        return self.user_name

# in this object or classs we will sva the data about complains that were submited by user
class complain(models.Model):
    complian_id=models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(customer,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    detail=models.TextField(max_length=500)
    complain_status=models.BooleanField(default=False)
    date=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.subject

#     in this class we have store the messages for that complain class for all the user
class message(models.Model):
    complain_id=models.ForeignKey(complain,on_delete=models.CASCADE)
    message=models.TextField(max_length=1000)
    # we have set this field for admin and customer we will use true for customer and false for admin
    reply=models.BooleanField()
    date=models.DateTimeField(default=datetime.now)


#
# this claa has the details of customer fee
class customer_fee(models.Model):
    customer_id=models.ForeignKey(customer,on_delete=models.CASCADE)
    fee_id = models.AutoField(primary_key=True)
    paid=models.BooleanField(default=False)
    start_date=models.DateTimeField()
    end_Date=models.DateField()
    total_amount=models.IntegerField()
    allow_installment=models.BooleanField(default=True)

    def __str__(self):
        return self.customer_id.user_name






