# Generated by Django 4.0 on 2022-06-05 19:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0024_message_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='stay_from',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
    ]
