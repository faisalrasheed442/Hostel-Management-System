from django.db import models

# Create your models here.

class customer(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=30)
    contact=models.CharField(max_length=20,default="")
    room=models.IntegerField(default=0)
    gender=models.CharField(max_length=30,default='Not Mentioned')
    Guardian_name=models.CharField(max_length=100)
    Guardian_contact=models.CharField(max_length=20)
    guardian_addrss=models.CharField(max_length=200)
    payment_staus=models.BooleanField()
    registration_date=models.DateField()
    user_image=models.ImageField(upload_to="static/profile_image",default="")

    def __str__(self):
        return self.user_name