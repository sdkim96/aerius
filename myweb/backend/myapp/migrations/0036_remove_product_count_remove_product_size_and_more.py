# Generated by Django 4.2.3 on 2023-09-19 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0035_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='count',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='is_preorder',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ProductSizeCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='myapp.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.product_size')),
            ],
        ),
    ]
