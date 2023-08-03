from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from django.utils import timezone as dj_timezone
from datetime import timedelta


class Message(models.Model):
    text = models.CharField(max_length=200)


class UserManager(BaseUserManager):
    def create_user(self, userid, password=None):
        if not userid:
            raise ValueError('Users must have a userid')
        user = self.model(
            userid=userid,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True, default='default_nickname')
    email = models.CharField(max_length=255, default='defaultemail@example.com')
    phone = models.CharField(max_length=20, default='01011111111')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'userid'


def utc_now_without_microseconds():
    return dj_timezone.now().replace(microsecond=0)

def utc_now_without_microseconds_plus_one_hour():
    return (dj_timezone.now() + timedelta(hours=1)).replace(microsecond=0)


class CustomToken(models.Model):
    customkey = models.CharField(max_length=255, unique=True)
    customuser = models.ForeignKey('User', on_delete=models.CASCADE, related_name='tokens')
    customcreated = models.DateTimeField(auto_now_add=False, default=utc_now_without_microseconds)
    customexp = models.DateTimeField(default=utc_now_without_microseconds_plus_one_hour)


class Staff(models.Model):
    staff_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_superuser = models.BooleanField(default=False)
    is_high_staff = models.BooleanField(default=False)
    is_low_staff = models.BooleanField(default=False)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_front = models.CharField(max_length=255)
    address_back = models.CharField(max_length=255)
    notices = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField()
    image = models.URLField(max_length=2000, blank=True, null=True)


class QnA(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField()
    image = models.URLField(max_length=2000, blank=True, null=True)


class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    contents = models.TextField()
    image = models.URLField(max_length=2000, blank=True, null=True)


class Discount(models.Model):
    percent = models.IntegerField()


class Product_Size(models.Model):
    name = models.CharField(max_length=20)


class Product_Type(models.Model):
    name = models.CharField(max_length=20)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.ForeignKey(Product_Type, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    size = models.ForeignKey(Product_Size, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    info = models.TextField(default='')


class ProductImage(models.Model):
    image = models.ImageField(default='product_images/default.jpg', upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Each_Product(models.Model):
    final_price = models.IntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Cart(models.Model):
    quantity = models.IntegerField()
    each_product = models.ForeignKey('Each_Product', on_delete=models.CASCADE)
