# Generated by Django 4.2.3 on 2023-07-28 01:02

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_remove_customtoken_customexp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customtoken',
            name='customexp',
            field=models.DateTimeField(default=myapp.models.utc_now_without_microseconds),
        ),
    ]
