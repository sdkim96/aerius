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

import jwt
class WhoAreYouView(APIView):
    
    def post(self, request, *args, **kwargs):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.replace('Bearer ', '')

        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded.get('user_id')
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(userid=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WhoAreYouSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

        # serializer_class = WhoAreYouSerializer
        # permission_classes = [IsAuthenticated]
