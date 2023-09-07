from rest_framework import viewsets,status
from ..models import *
from ..serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

class StoreViewSet(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []  # Uncomment this if you want to add authentication
    permission_classes = [AllowAny]
    

