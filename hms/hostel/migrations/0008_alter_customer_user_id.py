# Generated by Django 4.0 on 2022-05-08 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0007_remove_customer_id_customer_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
