# Generated by Django 3.0.8 on 2020-09-19 17:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0051_auto_20200919_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='testid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]