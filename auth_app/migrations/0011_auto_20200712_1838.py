# Generated by Django 3.0.8 on 2020-07-12 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0010_auto_20200712_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='id',
            field=models.CharField(default='bd822d62-c440-11ea-a8f4-402343e1102e', max_length=200, primary_key=True, serialize=False),
        ),
    ]
