# Generated by Django 4.2.3 on 2023-09-27 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0037_remove_cart_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
