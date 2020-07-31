# Generated by Django 3.0.8 on 2020-07-31 16:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0029_educationportal'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('userid', models.CharField(max_length=100)),
                ('attendancedate', models.DateField()),
                ('status', models.CharField(max_length=1)),
            ],
        ),
    ]
