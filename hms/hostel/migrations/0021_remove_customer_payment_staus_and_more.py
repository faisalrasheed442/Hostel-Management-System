# Generated by Django 4.0 on 2022-06-03 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0020_rename_user_id_customer_fee_fee_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='payment_staus',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='registration_date',
        ),
    ]
