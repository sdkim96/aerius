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
    size_count_mapping = serializers.JSONField(write_only=True, required=False)
    type_id = serializers.IntegerField(write_only=True)
    main_image = serializers.ImageField(write_only=True)
    switching_image = serializers.ImageField(write_only=True)
    sub_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'type_id', 'price', 
                   'info','main_image', 'switching_image', 
                   'sub_images', 'size_count_mapping']

    def create(self, validated_data):
        type_id = validated_data.pop('type_id')
        main_image_data = validated_data.pop('main_image')
        switching_image_data = validated_data.pop('switching_image')
        sub_images_data = validated_data.pop('sub_images')
        size_count_mapping = validated_data.pop('size_count_mapping', {})

        product_type = Product_Type.objects.get(id=type_id)

        # 이제 `validated_data`는 `Product` 모델에 직접 매핑되는 필드만 포함하고 있습니다.
        product = Product.objects.create(
            type=product_type,
            **validated_data
        )

        # 이후 로직은 이전과 동일합니다.
        for size, count in size_count_mapping.items():
            product_size, _ = Product_Size.objects.get_or_create(name=size)
            ProductSizeCount.objects.create(
                product=product,
                size=product_size,
                count=int(count)
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


class ProductSizeCountSerializer(serializers.ModelSerializer):
    size = ProductSizeSerializer(read_only=True)
    
    class Meta:
        model = ProductSizeCount
        fields = ['size', 'count']


class ProductSerializer(serializers.ModelSerializer):
    type = ProductTypeSerializer(read_only=True)
    sizes = ProductSizeCountSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'type', 'price', 'info', 'images', 'sizes']


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    imageURL = serializers.SerializerMethodField()  # SerializerMethodField 사용
    name = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    size = serializers.CharField()
    quantity = serializers.IntegerField(read_only=True)  # 수량 필드 추가

    class Meta:
        model = CartItem
        fields = ['product_id', 'imageURL', 'name', 'price', 'size', 'quantity']

    def get_imageURL(self, obj):
        if obj.product.images.first():
            return obj.product.images.first().image.url
        return None
    
    def get_name(self, obj):
        return obj.product.name


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items']

    def create(self, validated_data):
        print("Entering CartSerializer create...")
        
        cart_items_data = validated_data['cart_items']  # 여기에서 .pop() 사용 안함
        
        cart, created = Cart.objects.get_or_create(user=self.context['request'].user, defaults=validated_data)
        print(f"Cart object: {cart}, Created: {created}")
        
        for cart_item_data in cart_items_data:
            product_id = int(cart_item_data['product_id'])  # 여기에서 .pop() 사용 안함
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} does not exist.")
            
            print(f"Processing product_id: {product_id}, product: {product}")
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, size=cart_item_data['size'], defaults=cart_item_data)

            print(f"CartItem object: {cart_item}, Created: {created}")

            if not created:
                cart_item.quantity += 1
            else:
                cart_item.price = product.price
                cart_item.quantity = 1
            cart_item.save()
            print(f"Updated CartItem object: {cart_item}")

        return cart





