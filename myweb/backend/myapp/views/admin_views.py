from ..serializers import *
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from rest_framework import viewsets, status
from ..utils.utils import Utils
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
# from ..admin.decorator_of_views import IsStaffUser
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

# Serializer에서 context를 사용하는 주된 이유는 Serializer가 현재 요청(request), 로그인된 사용자 등의 추가적인 정보를 알 필요가 있을 때입니다. Serializer 자체는 HTTP 요청에 대한 정보를 알지 못하기 때문에, 이 정보를 context를 통해 전달받습니다.

# 이는 다음과 같은 경우에 유용합니다:

# 현재 로그인한 사용자 정보가 필요한 경우: 일부 API는 로그인한 사용자의 정보에 따라 다르게 동작할 수 있습니다. 예를 들어, 일부 필드는 특정 사용자가 로그인한 경우에만 직렬화되거나 역직렬화될 수 있습니다.

# 현재 요청(request) 객체가 필요한 경우: 요청 객체는 요청에 대한 상세한 정보를 포함하고 있습니다. 이 정보는 HTTP 메소드(GET, POST, PUT 등), 요청의 헤더, 요청의 본문 등을 알아낼 때 필요합니다.

# 다른 추가적인 정보가 필요한 경우: context는 다른 추가적인 정보를 전달하는 데도 사용할 수 있습니다. 이 정보는 Serializer의 동작에 영향을 미칠 수 있습니다.

# 예를 들어, 위에서 언급한 ProductRegisterSerializer의 경우, 이미지 파일을 처리하기 위해 요청 객체가 필요합니다. 이 요청 객체는 context를 통해 Serializer에 전달됩니다.

class ProductRegisterView(APIView):
    
    def post(self, request):
        try:
            print(request.data)
        
            # Create a copy of the request data
            data = request.data.copy()
            
            # Rename the keys in the data
            data['name'] = data.pop('productName')[0]
            
            # Create or get product type
            product_type, _ = Product_Type.objects.get_or_create(name=data.pop('productType')[0])
            data['type_id'] = product_type.id
            
            # Create or get product size
            product_size, _ = Product_Size.objects.get_or_create(name=data.pop('productSize')[0])
            data['size_id'] = product_size.id

            data['count'] = int(data.pop('productCount')[0])  # 변경됨
            data['info'] = data.pop('productInfo')[0]  # 변경됨
            data['price'] = int(data.pop('productPrice')[0])  # 변경됨
            
            # Add images
            data['main_image'] = request.FILES.get('mainImage')
            data['switching_image'] = request.FILES.get('switchingImage')
            sub_images_list = [request.FILES.get(f'subImage{i}') for i in range(3) if f'subImage{i}' in request.FILES]
            data['sub_images'] = sub_images_list[0]

            print('sub : ', data['sub_images'])


            
            # Initialize the serializer with the renamed data and context
            print("serialized data : ", data)
            serializer = ProductCreateSerializer(data=data, context={'request': request})
            
            # Validate and save the data
            if serializer.is_valid():
                print("Data is valid. Saving...")
                print(f"Product type ID: {product_type.id}")
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # Log the validation errors
            print("Validation errors:")
            print(serializer.errors)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


class ProductReadallView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []  # Uncomment this if you want to add authentication
    permission_classes = [AllowAny]  # Uncomment this if you want to add permissions



class ProductReadOneView(RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(UpdateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Set `partial=True` to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



