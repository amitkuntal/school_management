# Generated by Django 3.0.8 on 2020-08-01 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0030_employeeattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 8, 1)),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='status',
            field=models.CharField(default='A', max_length=1),
        ),
    ]