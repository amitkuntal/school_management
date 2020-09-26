# Generated by Django 3.0.8 on 2020-09-26 04:24

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0055_auto_20200922_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveClass',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('roomid', models.UUIDField(default=uuid.uuid4)),
                ('link', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 9, 26)),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 9, 26)),
        ),
        migrations.AlterField(
            model_name='homework',
            name='homeworkdate',
            field=models.DateField(default=datetime.date(2020, 9, 26)),
        ),
        migrations.AlterField(
            model_name='test',
            name='expiredate',
            field=models.DateField(default=datetime.date(2020, 9, 26)),
        ),
    ]