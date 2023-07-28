# Generated by Django 4.2.3 on 2023-07-26 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_address_good_isgood_isgoods_delete_admin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='default_nickname', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='01011111111', max_length=15),
        ),
    ]
