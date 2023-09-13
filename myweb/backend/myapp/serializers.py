from rest_framework import serializers
from .models import *
from django.conf import settings

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


class ProductCreateSerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(write_only=True)
    size_id = serializers.IntegerField(write_only=True)
    main_image = serializers.ImageField(write_only=True)
    switching_image = serializers.ImageField(write_only=True)
    sub_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'type_id', 'price', 'size_id', 'count', 'info', 'main_image', 'switching_image', 'sub_images']

    def create(self, validated_data):
        type_id = validated_data.pop('type_id')
        size_id = validated_data.pop('size_id')
        main_image_data = validated_data.pop('main_image')
        switching_image_data = validated_data.pop('switching_image')
        sub_images_data = validated_data.pop('sub_images')

        product_type = Product_Type.objects.get(id=type_id)
        product_size = Product_Size.objects.get(id=size_id)

        product = Product.objects.create(
            type=product_type,
            size=product_size,
            **validated_data
        )

        ProductImage.objects.create(
            image=main_image_data,
            product=product
        )

        ProductImage.objects.create(
            image=switching_image_data,
            product=product
        )

        for sub_image_data in sub_images_data:
            ProductImage.objects.create(
                image=sub_image_data,
                product=product
            )

        return product



class ProductSerializer(serializers.ModelSerializer):
    type = ProductTypeSerializer(read_only=True)
    size = ProductSizeSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'type', 'price', 'size', 'count', 'info', 'images']
