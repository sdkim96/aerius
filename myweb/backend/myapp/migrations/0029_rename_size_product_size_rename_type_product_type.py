# Generated by Django 4.2.3 on 2023-07-31 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_discount_size_type_product_each_product_cart'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Size',
            new_name='Product_Size',
        ),
        migrations.RenameModel(
            old_name='Type',
            new_name='Product_Type',
        ),
    ]
