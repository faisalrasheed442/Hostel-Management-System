# Generated by Django 4.0 on 2022-05-22 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0017_rooms_current_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='complain_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='hostel.complain'),
            preserve_default=False,
        ),
    ]
