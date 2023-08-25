from rest_framework import serializers
from .models import *

# Django와 Django Rest Framework에서 Meta 클래스는 모델이나 시리얼라이저의 메타데이터를 정의하는 데 사용됩니다. 
# 이 Meta 클래스는 Django 모델이나 시리얼라이저 클래스 내부에 중첩 클래스로서 정의되며, 해당 모델이나 시리얼라이저에 대한 추가적인 정보를 제공합니다.
#모델의 Meta 클래스에서는 데이터베이스 테이블 이름, 정렬 순서, 기본 키 등을 정의할 수 있습니다. 예를 들어:


# 1. User 모델 검증하는 클래스
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userid', 'nickname', 'password', 'email', 'phone')


class UserLoginSerializer(serializers.ModelSerializer):
    userid = serializers.CharField()  # 필드의 스키마를 오버라이딩하는거임

    class Meta:
        model = User
        fields = ('userid', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class WhoAreYouSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userid', 'password', 'nickname', 'email', 'phone', 'created_at']



# 2. Message 모델 검증하는 클래스
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'



# 3
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Type
        fields = ['name']

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Size
        fields = ['name']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    type = ProductTypeSerializer(read_only=True)
    size = ProductSizeSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'type', 'price', 'size', 'count', 'info', 'images']
