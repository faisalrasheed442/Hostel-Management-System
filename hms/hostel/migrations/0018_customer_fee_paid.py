# Generated by Django 4.0 on 2022-06-01 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0017_rooms_current_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_fee',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
