from rest_framework import viewsets,status
from ..models import *
from ..serializers import *

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Each_Product.objects.all()
    each_product = Each_ProductsSerializer()
    


