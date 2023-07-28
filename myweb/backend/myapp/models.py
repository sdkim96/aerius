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


# 스키마 1 : 유저의 정보와 관련된 정보 

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True, default='default_nickname')
    email = models.CharField(max_length=255, default='defaultemail@example.com')
    phone = models.CharField(max_length=20, default='01011111111')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'userid'


# 일대 다인 경우엔 '다'쪽이 '일'의 외래키를 참조하는거라서 굳이 User에 token관련 필드가
# 존재하지 않아도 괜찮다.

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
    is_superuser = models.BooleanField(default=False)  # 모든 권한 (highstaff에 명령까지 엑세스 가능)
    is_high_staff = models.BooleanField(default=False)  # 유저관리, 상품관리, 홍보, 지원, 보안까지 엑세스 가능
    is_low_staff = models.BooleanField(default=False)  # 홍보, 지원관리만 엑세스 가능


    

    


# 실제로 mysql 디비에서 칼럼명이 custom_user_id로 저장되는 이유
# Token 모델에서 custom_user 필드는 OneToOneField로 정의되었으므로, Django는 이 필드에 대응하는 custom_user_id라는 컬럼을 데이터베이스에 생성합니다. 이 컬럼은 User 모델의 행을 참조하는 외래키이며, 
# 필드명 뒤에 _id를 붙여서 컬럼명을 만드는 것은 Django의 규칙입니다.


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_front = models.CharField(max_length=255)
    address_back = models.CharField(max_length=255)
    notices = models.TextField()  # 주문시 유의사항
    updated_at = models.DateTimeField(auto_now=True)


# 스키마 2 : 물품의 정보와 관련된 정보

class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255) 
    types = models.CharField(max_length=255) 
    price = models.IntegerField()


class Good(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    quantity = models.IntegerField() 


class IsGoods(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    is_soldout = models.BooleanField(default=False)
    is_forsale = models.BooleanField(default=False)


class IsGood(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_soldout = models.BooleanField(default=False)
    is_forsale = models.BooleanField(default=False)
    sold_at = models.DateTimeField(auto_now_add=True)


# 스키마 3 : helppage와 관련된 스키마

class Review(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField를 사용하여 자동 증가 ID 설정
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField()  # TextField 사용
    image = models.URLField(max_length=2000, blank=True, null=True)  # URLField 사용, 이미지는 선택적일 수 있으므로 blank=True, null=True 설정


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


# aerius.auth_group: Django의 기본 인증 시스템에서 사용하는 테이블로, 사용자들을 그룹으로 분류하는데 사용됩니다. 이는 권한 관리를 쉽게하기 위한 기능입니다.

# aerius.auth_group_permissions: 각 그룹이 가진 권한을 저장하는 테이블입니다.

# aerius.auth_permission: Django에서 제공하는 권한을 정의하는 테이블입니다. 사용자 또는 그룹에게 이 테이블에 정의된 권한을 할당할 수 있습니다.

# aerius.auth_user: 사용자의 인증 정보를 저장하는 테이블로, 커스텀 User 모델을 정의하였습니다. 여기에는 사용자의 이름과 비밀번호, 계정 생성일이 포함됩니다.

# aerius.auth_user_groups: 사용자와 그룹 사이의 관계를 정의하는 테이블입니다. 이 테이블을 통해 각 사용자가 어떤 그룹에 속해 있는지 알 수 있습니다.

# aerius.auth_user_user_permissions: 사용자별로 할당된 권한을 저장하는 테이블입니다.

# aerius.django_admin_log: Django 관리자 사이트에서의 사용자 활동을 기록하는 테이블입니다.

# aerius.django_content_type: Django에서 사용하는 내용 유형을 저장하는 테이블로, 주로 권한 관리에 사용됩니다.

# aerius.django_migrations: Django에서 데이터베이스 마이그레이션의 히스토리를 기록하는 테이블입니다.

# aerius.django_session: Django에서 세션 데이터를 저장하는 테이블입니다.

# aerius.myapp_issold: 판매된 상품과 관련된 정보를 저장하는 테이블입니다. 특정 상품이 어떤 사용자에 의해 언제 판매되었는지, 그리고 판매 여부 등의 정보가 포함됩니다.

# aerius.myapp_goodstype: 상품의 유형을 정의하는 테이블입니다.

# aerius.myapp_goods: 상품에 대한 정보를 저장하는 테이블입니다. 상품 이름, 유형, 가격, 그리고 상품을 등록한 사용자에 대한 정보가 포함됩니다.

# aerius.myapp_admin: 관리자 정보를 저장하는 테이블로, 총 판매량과 총 수익 등의 정보가 포함됩니다.

# aerius.myapp_message: 메시지 정보를 저장하는 테이블로, 문자열 형태의 메시지를 저장합니다.

# aerius.myapp_user: 커스텀 User 모델로서, 사용자의 인증 정보를 저장하는 테이블입니다.