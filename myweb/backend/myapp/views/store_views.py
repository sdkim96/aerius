from rest_framework import viewsets,status
from ..models import *
from ..serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import Http404  # Import Http404

from django.conf import settings
myweb = settings.WEB_DOMAIN_URL

class StoreViewSet(ListAPIView):
    queryset = Product.objects.all()
    print(queryset)
    serializer_class = ProductSerializer
    authentication_classes = []  # Uncomment this if you want to add authentication
    permission_classes = [AllowAny]
    

class EachStoreViewSet(ListAPIView):
    
    authentication_classes = []  # Uncomment this if you want to add authentication
    permission_classes = [AllowAny]

    def get(self, request, pk=None, *args, **kwargs):  # pk 인자 추가
        try:
            queryset = Product.objects.get(id=pk)  # pk를 사용해 쿼리
            serializer = ProductSerializer(queryset)  # 직렬화
            serializer_data = serializer.data

            # 이미지 URL에 도메인 부분 추가
            for image_dict in serializer_data['images']:
                image_dict['image'] = f"{settings.WEB_DOMAIN_URL}{image_dict['image']}"

            return Response(serializer_data, status=status.HTTP_200_OK)  # 응답
        except Product.DoesNotExist:  # 예외 처리
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        
        
