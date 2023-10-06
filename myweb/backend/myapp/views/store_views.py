from rest_framework import viewsets,status
from ..models import *
from ..serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import Http404  # Import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q

from django.conf import settings
myweb = settings.WEB_DOMAIN_URL

class StoreViewSet(ListAPIView):
    queryset = Product.objects.all()
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


class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        print("Request data:", request.data)  # 로깅: 요청 데이터 확인

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)  # 로깅: Serializer의 유효성 검사 오류 확인
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartRetrieveView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    

    def get_object(self):
    # 현재 사용자의 장바구니를 반환합니다.
        user = self.request.user
        cart = Cart.objects.get(user=user)

        # Cart 객체의 자세한 내용을 출력
        print(f"Cart ID: {cart.id}, User: {cart.user}")
        for item in cart.cart_items.all():
            print(f"  - Product ID: {item.product_id}, Name: {item.product.name}, Price: {item.price}, Size: {item.size}, Quantity: {item.quantity}")

        return cart


# views.py

class CartItemRemoveOneView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        product_id = self.kwargs.get('product_id')
        size = self.kwargs.get('size')
        return get_object_or_404(CartItem, product__id=product_id, size=size)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.quantity > 1:
            instance.quantity -= 1
            instance.save()
            return Response(status=status.HTTP_200_OK)
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemRemoveAllView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        product_id = self.kwargs.get('product_id')
        size = self.kwargs.get('size')
        return get_object_or_404(CartItem, product__id=product_id, size=size)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class SearchItemViewSet(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        query = self.request.data.get('query', "")
        return Product.objects.filter(Q(name__icontains=query))

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)