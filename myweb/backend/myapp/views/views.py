from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Message, User, CustomToken
from ..serializers import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
import jwt
import logging



from ..database.CRUD import CrudUser as D
from ..database.TokenFactory import TokenFactory as T



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


from rest_framework.permissions import AllowAny


class LoginViewSet(APIView):
    authentication_classes = []  # Here: don't use any authentication for this view
    permission_classes = [AllowAny]  # And allow any user (authenticated or not) to access this view
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

            # 토큰을 해독하여 사용자의 권한을 읽습니다.
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            level = decoded.get('level')

            # 사용자의 권한을 응답에 포함시킵니다.
            return Response({"token": token, "level": level}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


logger = logging.getLogger(__name__)

class LogoutViewSet(APIView):

    def post(self, request, *args, **kwargs):
        logger.info(f"Request data: {request.data}")
        
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.warning("Authorization header missing")
            return Response({'error': 'Authorization header missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Strip off 'Bearer '
        token = auth_header.replace('Bearer ', '')
        
        result = T.remove_token(token)
        if "result" in result:
            return Response(status=status.HTTP_200_OK)
        else:
            logger.error("Internal server error while removing token")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


class AuthorizedViewSet(APIView): 

    def post(self, request, *args, **kwargs):

        work = request.data.get('work')  # 클라이언트가 요청한 작업의 정보를 받아옵니다.
        auth_header = request.headers.get('Authorization')

        print(work)
        print(auth_header)

        token = auth_header.replace('Bearer ', '')  # 'Bearer '를 제거하여 토큰만을 추출합니다.
        print(token)

        result = T.is_authorized(token=token, work=work)
        
        if result:
            return Response({'result' : '유효합니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error' : '유효하지 않습니다'}, status=status.HTTP_401_UNAUTHORIZED)

        
        

