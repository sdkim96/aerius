from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Message, User, CustomToken
from .serializers import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .database.CRUD import CrudUser as D
from .database.TokenFactory import TokenFactory as T


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


# 유저가 가입할때 쓰는 로직임.
class CheckUserViewSet(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                crud_user = D(request.data)  # 인스턴스 생성
                crud_user.create()
            except Exception as e:
                print(e)
            finally:
                print("저장완료")

            return Response({"message": "Userid available"}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            errors = serializer.errors
            
            if 'userid' in errors.keys() and 'nickname' not in errors.keys():
                print('error1')
                return Response({"error" : "아이디가 중복됩니다."})
            elif 'userid' not in errors.keys() and 'nickname' in errors.keys():
                print('error2')
                return Response({"error" : "닉네임이 중복됩니다."})
            else:
                print('error3')
                return Response({"error" : "유저아이디와 닉네임 둘다 중복됩니다."})


class LoginViewSet(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        thisuser = authenticate(userid=serializer.validated_data['userid'], password=serializer.validated_data['password'])

        if thisuser:
            # 사용자를 데이터베이스에 저장합니다.
            token, exp = T.create_token(thisuser)
            CustomToken.objects.create(customuser=thisuser, customkey=token, customexp=exp)
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutViewSet(APIView):

    def post(self, request, *args, **kwargs):
        print(request.data)
        
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        
        # Strip off 'Bearer '
        token = auth_header.replace('Bearer ', '')
        
        result = T.remove_token(token)
        if "result" in result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AdminLevelViewSet(APIView):

    def post(self, request, *args, **kwargs):
        pass

