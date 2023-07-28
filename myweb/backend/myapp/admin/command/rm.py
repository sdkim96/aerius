# 아래 코드들은 수퍼사용자 권한이 있어야 사용할 수 있습니다.
from ...models import *

class SuperUser:
    
    # 아래 생성자에 수퍼유저임을 확인할 수 있는 로직을 차후에 구현하세요
    def __init__(self, sudo):
        self.sudo = sudo


    @staticmethod
    def remove_all_tokens(self):
        tokens_count = CustomToken.objects.all().count()
        CustomToken.objects.all().delete()
        return ({"result" : f"서버의 모든 토큰({tokens_count}개)이 삭제되었습니다."})