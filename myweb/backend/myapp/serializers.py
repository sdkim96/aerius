from rest_framework import serializers
from .models import User, Message

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



# 2. Message 모델 검증하는 클래스
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'