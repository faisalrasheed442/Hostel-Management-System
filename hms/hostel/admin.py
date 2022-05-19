from django.contrib import admin
from .models import customer,rooms,customer_fee
# Register your models here.
admin.site.register(customer)
admin.site.register(rooms)
admin.site.register(customer_fee)