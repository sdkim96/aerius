from secrets import token_hex
from django.utils import timezone
from datetime import datetime, timedelta, timezone
from ..models import User, CustomToken
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import jwt
import logging

logger = logging.getLogger(__name__)

class TokenFactory:

    @staticmethod
    def create_token(user):
        payload = {
            'user_id': user.userid,  
            'exp': datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=1)
        }
        token = jwt.encode(payload, 'settings.SECRET_KEY', algorithm='HS256')
        exp = (datetime.now(timezone.utc) + timedelta(hours=1)).replace(microsecond=0)
        
        return token, exp


    @staticmethod
    def check_token(token):

        now = datetime.now(timezone.utc)
        decoded = jwt.decode(token, 'settings.SECRET_KEY', algorithms=['HS256'])
        exp = datetime.fromtimestamp(decoded.get('exp'), tz=timezone.utc).replace(microsecond=0)

        try:
            if exp <= now:
                return {"error" : "사용자의 로그인 세션이 만료되었습니다."}
            else:
                check = CustomToken.objects.get(customkey=token)

        except Exception:
            return {"error" : "사용자의 토큰이 서버에 존재하지 않습니다."}
        
        if check:
            return True
        else:
            return False


    @staticmethod
    def remove_token(token):
        try:
            decoded = jwt.decode(token, 'settings.SECRET_KEY', algorithms=['HS256'])
            userid = decoded.get('user_id')
            user = User.objects.get(userid=userid)  # Retrieve the User instance
            exp = datetime.fromtimestamp(decoded.get('exp'), tz=timezone.utc).replace(microsecond=0)
            
            print(user, exp)

            current_server_token = CustomToken.objects.get(customexp=exp, customuser=user)
            current_server_token.delete()

            return {"result" : "서버의 토큰이 삭제되었습니다."}
        except User.DoesNotExist:
            return {"error" : "해당 사용자가 존재하지 않습니다."}
        except CustomToken.DoesNotExist:
            return {"error" : "서버에 해당 사용자의 토큰이 존재하지 않습니다."}
        except Exception as e:
            # Log the error if anything unexpected happens
            logger.error(f"Unexpected error in remove_token: {e}")
            return {"error" : str(e)}


    # 아래 두 메소드는 차후에 admin.rm 모듈로 편입할 예정입니다.

    @staticmethod
    def token_expired():

        tokenalldatas = CustomToken.objects.all()
        now = datetime.now(timezone.utc)

        expired_datas = []
        for t in tokenalldatas:
            if t.customexp < now:
                expired_datas.append(t.customexp)

        for d in expired_datas:
            delete_tokens = CustomToken.objects.filter(customexp=d)
            delete_tokens.delete()
 
        return {"result" : f"서버에 {len(expired_datas)}개의 토큰이 삭제되었습니다."}
    
    
    @staticmethod
    def remove_all_tokens():
        tokens_count = CustomToken.objects.all().count()
        CustomToken.objects.all().delete()
        return {"result" : f"서버의 모든 토큰({tokens_count}개)이 삭제되었습니다."}
