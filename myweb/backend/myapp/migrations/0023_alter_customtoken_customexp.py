# Generated by Django 4.2.3 on 2023-07-28 01:04

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_customtoken_customexp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customtoken',
            name='customexp',
            field=models.DateTimeField(default=myapp.models.utc_now_without_microseconds_plus_one_hour),
        ),
    ]
