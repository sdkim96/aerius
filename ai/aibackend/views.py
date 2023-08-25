from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from .crud import *
from .models import *
from .settings import SECRET_KEY
from pydantic import BaseModel
from ai.myapp.chatbot.models.intent_module import IntentModel
from ai.myapp.chatbot.models.ner_module import NerModel
from ai.myapp.chatbot.utils.Preprocess import Preprocess
import jwt

class ChatbotQuery(BaseModel):
    query: str

response_string = """대답은 적절히 출력될거입니다. 
        고려해야할 사항
        1. 쿼리를 보내는 사람이 누군지
        2. 쿼리를 받아서 모델에 넣어야함
        3. 그 쿼리에 대한 답으로 sql서버에 접근해야함
        4. sql 서버에서 적절히 해야함"""

def get_userid(authorization: str = Header(None)) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing token")
    # 토큰은 "Bearer [토큰값]" 형식으로 전송됨
    token_type, token_value = authorization.split()
    if token_type.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token type")
    else:
        token = jwt.decode(token_value, SECRET_KEY, algorithms=['HS256'])
        print(token)
        userid = token.get('user_id')
        print(userid)
    return userid

def making_response(name, intent, ner):
    intents = {
        0: "주문",
        1: "배송",
        2: "매장",
        3: "AS",
        4: "제품_정보",
        5: "제품_재고"
    }
    
    # 기본 응답 설정
    response = f"{name}님, 안녕하세요. {intents[intent]} 확인을 원하시는군요. "
    
    # 조건에 따라 응답을 추가로 생성
    if 1 in ner.values() and intent == 1:
        delivery_time = ' '.join([k for k, v in ner.items() if v == 1])
        response += f"당신의 배송시간은 {delivery_time}에 맞춰 진행하겠습니다."
    elif 3 in ner.values() and intent == 2:
        location = ' '.join([k for k, v in ner.items() if v == 3])
        response += f"가까운 매장은 {location}에 위치해 있습니다."
    elif 4 in ner.values() and intent == 4:
        product = ' '.join([k for k, v in ner.items() if v == 4])
        response += f"{product}에 대한 정보를 알려드리겠습니다."
    elif 5 in ner.values() and intent == 5:
        size = ' '.join([k for k, v in ner.items() if v == 5])
        response += f"{size} 사이즈의 재고를 확인해 드리겠습니다."
    else:
        response += "자세한 사항은 고객센터로 문의해주세요."
        
    return response



    



async def post_query(chatbot_query: ChatbotQuery, userid: str = Depends(get_userid), db: Session = Depends(get_db)):
    q = chatbot_query.query
    print(q)

    p = Preprocess(userdic='/home/azureuser/projects/aerius/ai/myapp/chatbot/dict/userdic.txt')
    intent = IntentModel(model='/home/azureuser/projects/aerius/ai/myapp/chatbot/models/models/230817_intent.h5',
                preprocess=p, tokenizer_path='/home/azureuser/projects/aerius/ai/myapp/chatbot/models/tokenizers/230817_intent_labeled_by_6_tokenizer.json')
    ner = NerModel(model='/home/azureuser/projects/aerius/ai/myapp/chatbot/models/models/230823_ner_model.h5',
                preprocess=p, tokenizer_path='/home/azureuser/projects/aerius/ai/myapp/chatbot/models/tokenizers/230822_ner_tagging_tokenizer.json')

    ner_predict= ner.predict_class(q)
    intent_predict= intent.predict_class(q)

    print('ner : ',ner_predict)
    print('ner type : ',type(ner_predict))
    print('intent : ',intent_predict)
    print('intent type : ',type(intent_predict))

    crud = Crud(table=Chatbot)
    new_chatbot_instance = Chatbot(name=userid, query=q, 
                                    intent=intent_predict,
                                    ner = ner_predict)  # Chatbot 모델의 인스턴스 생성


    try:
        crud.create_item(item=new_chatbot_instance, db=db)  # 인스턴스를 넘겨줌

    except Exception as e:
        print(e)
        return {"error": str(e)}
    
    response=making_response(name=userid, intent=intent_predict, ner=ner_predict)

    return {"response": response}

