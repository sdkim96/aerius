from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.views import *
from ..views.store_views import *

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'store', StoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkuser/', CheckUserViewSet.as_view(), name='checkuser'),
    path('login/', LoginViewSet.as_view(), name='login'),  # Add this line
    path('logout/', LogoutViewSet.as_view(), name='logout'),  # Add this line
    path('authorize/', AuthorizedViewSet.as_view(), name='authorize'),
]
