from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.views import *
from ..views.user_views import *
from ..views.admin_views import *

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

# path('user/', include('myapp.urls.user_urls')),

urlpatterns = [
    path('', include(router.urls)),
    path('whoareyou/', WhoAreYouView.as_view(), name='whoareyou'),
]
