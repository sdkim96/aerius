from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.views import *
from ..views.store_views import *
from ..views.admin_views import *

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

# path('admin/', include('myapp.urls.admin_urls')),

urlpatterns = [
    path('', include(router.urls)),
    path('products/register/', ProductRegisterView.as_view(), name='product-register'),
    path('products/read/all/', ProductReadallView.as_view(), name = 'product-read-all'),
    path('products/read/<int:pk>/', ProductReadOneView.as_view(), name = 'product-read-all'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name = 'product-read-all'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name = 'product-read-all'),
]
