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


# product와 관련된 스키마

class Product_Size(models.Model):
    name = models.CharField(max_length=20)


class Product_Type(models.Model):
    name = models.CharField(max_length=20)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.ForeignKey(Product_Type, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    info = models.TextField(default='')
    is_preorder = models.BooleanField(default=False)


class ProductSizeCount(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.ForeignKey(Product_Size, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)



class ProductImage(models.Model):
    image = models.ImageField(default='product_images/default.jpg', upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


# Cart 모델 추가
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


# CartItem 모델 추가
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=50, default='')


    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status_choices = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    size = models.ForeignKey(Product_Size, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

