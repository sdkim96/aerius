from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkuser/', CheckUserViewSet.as_view(), name='checkuser'),
    path('login/', LoginViewSet.as_view(), name='login'),  # Add this line
    path('logout/', LogoutViewSet.as_view(), name='logout'),  # Add this line
    path('adminlevel/', AdminLevelViewSet.as_view(), name='adminlevel'),
]
